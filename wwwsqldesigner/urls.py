from django.conf.urls.defaults import *

urlpatterns = patterns('wwwsqldesigner.views',
    url(r'^$', 'index', name='wwwsqldesigner_index'),
    url(r'^backend/php-mysql/$', 'getdb', name='wwwsqldesigner_getdb'),
)
