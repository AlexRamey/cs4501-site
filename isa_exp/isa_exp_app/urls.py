from django.conf.urls import url
from .views import index, searchresults, hotitems

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^searchresults/$', searchresults),
    url(r'^hotitems/$', hotitems),
]