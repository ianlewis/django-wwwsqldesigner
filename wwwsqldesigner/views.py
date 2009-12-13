from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.db.models import get_models
from django.db.models import ForeignKey, ManyToManyField
from django.utils.importlib import import_module

def map_db():
    from wwwsqldesigner.settings import DB_MAP
    try:
        return DB_MAP[settings.DATABASE_ENGINE.split(".")[-1]]
    except IndexError:
        return 'mysql'

def index(request):
    return direct_to_template(request, "wwwsqldesigner/index.html", {})

def config(request):
    return direct_to_template(request, "wwwsqldesigner/config.js", {
        'default_db': map_db(),
    }, mimetype="text/javascript")

def getdb(request):
    app_name = request.GET.get("database")
    app_mod = None
    if app_name != "django":
        try:
            app_mod = import_module(app_name+".models")        
        except ImportError:
            pass
    table_list = []

    for model in get_models(app_mod):
        fields_list = []
        key_list = []

        for field in model._meta.fields:
            attname,column = field.get_attname_column()
            if field.primary_key:
                key_list.append({
                    "type": "primary",  
                    "field_name": column,
                })
            if field.unique:
                key_list.append({
                    "type": "unique",
                    "field_name": column,
                })
                
            field_dict = {
                "name": column,
                "null": field.null,
                "datatype": field.db_type(),
                #"default": field.default,
                "comment": field.verbose_name,
            }
            if isinstance(field, ForeignKey): 
                rel_field_name = field.rel.field_name
                for rel_table_field in field.rel.to._meta.fields:
                    if rel_table_field.name == field.rel.field_name:
                        rel_attname,rel_field_name = rel_table_field.get_attname_column()

                field_dict["relation"] = {
                    "table_name": field.rel.to._meta.db_table,
                    "field_name": rel_field_name,
                }
            #TODO: Support ManyToMany fields
            fields_list.append(field_dict)

        table_list.append({
            "name": model._meta.db_table,
            "fields": fields_list,
            "table_keys": key_list,
        })

    return direct_to_template(request, "wwwsqldesigner/dbschema.xml", {"tables": table_list}, mimetype="text/xml")
