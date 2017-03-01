from django.conf.urls import url
from .views import users, user, user_purchased, user_sold, user_selling
from .views import products, product
from .views import orders, order
from .views import productsnapshots, productsnapshot
from .views import conditions, condition
from .views import categories, category, category_products

from . import home

urlpatterns = [
    url(r'^$', home.index, name='index'),

    url(r'^users/$', users),
    url(r'^users/(?P<user_id>\d+)/$', user),
    url(r'^users/(?P<buyer_id>\d+)/purchased/$', user_purchased),
    url(r'^users/(?P<seller_id>\d+)/sold/$', user_sold),
    url(r'^users/(?P<seller_id>\d+)/selling/$', user_selling),
    url(r'^products/$', products),
    url(r'^products/(?P<product_id>\d+)/$', product),
    url(r'^orders/$', orders),
    url(r'^orders/(?P<order_id>\d+)/$', order),
    url(r'^productsnapshots/$', productsnapshots),
    url(r'^productsnapshots/(?P<productsnapshot_id>\d+)/$', productsnapshot),
    url(r'^conditions/$', conditions),
    url(r'^conditions/(?P<condition_id>\d+)/$', condition),
    url(r'^categories/$', categories),
    url(r'^categories/(?P<category_id>\d+)/$', category),
    url(r'^categories/(?P<category_id>\d+)/products/$', category_products),
]