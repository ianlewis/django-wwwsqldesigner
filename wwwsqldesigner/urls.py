from django.conf.urls.defaults import *

urlpatterns = patterns('wwwsqldesigner.views',
    url(r'^$', 'index', name='wwwsqldesigner_index'),
    url(r'^backend/django/$', 'getdb', name='wwwsqldesigner_getdb'),
    url(r'^config.js$', 'config', name='wwwsqldesigner_config'),
)
