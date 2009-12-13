var CONFIG = {
	AVAILABLE_DBS:["mysql","sqlite","web2py","mssql","postgresql"],
	DEFAULT_DB:"{{ default_db }}",

	AVAILABLE_LOCALES:["en","fr","de","cs","pl","pt_BR","es", "ru","eo"],
	DEFAULT_LOCALE:"en",
	
	AVAILABLE_BACKENDS:["django"],
	DEFAULT_BACKEND:["django"],

	RELATION_THICKNESS:2,
	RELATION_SPACING:15,
	
	STATIC_PATH: "{{ MEDIA_URL }}wwwsqldesigner/",
	XHR_PATH: "{% url wwwsqldesigner_index %}"
}
