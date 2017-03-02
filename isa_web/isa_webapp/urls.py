from django.conf.urls import url
from django.contrib import admin
from isa_webapp import views

urlpatterns = [
    url(r'^$', views.base, name='base'),

    url(r'^search/$',views.searchproduct, name='search'),

    url(r'^product/(?P<id>[0-9]+)/$',views.productdetails, name='product'),

    url(r'^profile/$',views.userprofile, name='profile'),
  ]