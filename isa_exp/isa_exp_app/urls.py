from django.conf.urls import url
from .views import index, search_results, hot_items, new_posts, product_details, user_profile, createaccount, login, createlisting, editlisting, recommendation

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^searchresults/$', search_results, name='searchresults'),
    url(r'^hotitems/$', hot_items),
    url(r'^newposts/$', new_posts),
    url(r'^productdetails/(?P<product_id>\d+)/$', product_details),
    url(r'^userprofile/(?P<user_id>\d+)/$', user_profile),
    url(r'^createaccount/$', createaccount),
    url(r'^login/$', login),
    url(r'^createlisting/$', createlisting),
    url(r'^editlisting/(?P<id>\d+)/$',editlisting),
    url(r'^recommendation/(?P<product_id>\d+)/$', recommendation),
]