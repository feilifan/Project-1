from django.conf.urls import patterns, include, url
from addr_book.views import class_apply,class_binfo,class_discuss,class_home,class_admin,class_delete,class_deal
from addr_book.views import class_deal_true,class_mainlist,class_register,class_seediscuss,class_selflist
from addr_book.views import class_admin_register,logout
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', class_home),
    (r'^/$',class_home),
    (r'^home/$',class_home),
    (r'^class_apply/$',class_apply),
    (r'^class_admin/$',class_admin),
    (r'^class_deal/$',class_deal),
    (r'^dealing/$',class_deal_true),
    (r'^class_binfo/$',class_binfo),
    (r'^logout/$',logout),
    (r'^delete/$',class_delete),
    (r'^class_discuss/$',class_discuss),
    (r'^class_mainlist/',class_mainlist),
    (r'^register/',class_register),
    (r'^admin_register/',class_admin_register),
    (r'^class_seediscuss/',class_seediscuss),
    (r'^class_selflist/',class_selflist),
    (r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    (r'^css/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT,}),
)