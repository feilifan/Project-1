from django.conf.urls import patterns, include, url
from views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'classms.views.home', name='home'),
    # url(r'^classms/', include('classms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$',test),
    url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH,}),
)
