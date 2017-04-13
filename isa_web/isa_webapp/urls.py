from django.conf.urls import url
from django.contrib import admin
from isa_webapp import views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^search/$',views.search, name='search'),
    url(r'^product/(?P<id>[0-9]+)/$',views.productdetails, name='product'),
    url(r'^profile/$',views.userprofile, name='profile'),
    url(r'^createaccount/$', views.createaccount, name='createaccount'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^createlisting/$', views.createlisting, name='createlisting'),
    url(r'^editlisting/(?P<id>[0-9]+)/$', views.editlisting, name='editlisting'),
  ]