from django.conf.urls import url
from .views import index, search_results, hot_items, product_details, user_profile, createaccount, login

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^searchresults/$', search_results),
    url(r'^hotitems/$', hot_items),
    url(r'^productdetails/(?P<product_id>\d+)/$', product_details),
    url(r'^userprofile/(?P<user_id>\d+)/$', user_profile),
    url(r'^createaccount/$', createaccount),
    url(r'^login/$', login),
]