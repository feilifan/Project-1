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
    url(r'^apply/$',m_apply),
    url(r'^binfo/$',binfo),
    url(r'^discuss/$',discuss),
    url(r'^home/$',home),
    url(r'^mainlist/$',mainlist),
    url(r'^register/$',register),
    url(r'^seediscuss/$',seediscuss),
    url(r'^selflist/$',selflist),
    url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH,}),
)
