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
    except KeyError:
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
            fields_list.append(field_dict)

        for m2m_field in model._meta.many_to_many:
            if m2m_field.rel.through:
                # If there is a through model then it will be added separately
                continue
            m2m_table_name = m2m_field.m2m_db_table()
            attname,model_pk_column = model._meta.pk.get_attname_column()
            to_model = m2m_field.rel.to
            attname,to_pk_column = to_model._meta.pk.get_attname_column() 

            # Add ManyToMany table
            table_list.append({
                "name": m2m_table_name,
                "fields": [
                    {
                        "name": "id",
                        "null": False,
                        "datatype": "integer",
                    },
                    {
                        "name": model.__name__.lower() + "_id",
                        "null": False,
                        "datatype": model._meta.pk.db_type(),
                        "relation": {
                            "table_name": model._meta.db_table,
                            "field_name": model_pk_column,
                        }
                    },
                    {
                        "name": to_model.__name__.lower() + "_id",
                        "null": False,
                        "datatype": to_model._meta.pk.db_type(),
                        "relation": {
                            "table_name": to_model._meta.db_table,
                            "field_name": to_pk_column,
                        }
                    },
                ],
                "keys": [
                    {
                        "type": "primary",  
                        "field_name": "id", 
                    },
                ],
            })


        table_list.append({
            "name": model._meta.db_table,
            "fields": fields_list,
            "table_keys": key_list,
        })

    return direct_to_template(request, "wwwsqldesigner/dbschema.xml", {"tables": table_list}, mimetype="text/xml")
