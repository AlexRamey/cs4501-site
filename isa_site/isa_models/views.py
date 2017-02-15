from django.shortcuts import render

from django.http import JsonResponse

from isa_models.models import User, Category, Condition, Product, ProductSnapshot, Order

from django.core import serializers 
import json
# Create your views here.

def index(request):
    return render(request, 'isa_site/index.html')

def users(request):
    return json_response(User.objects.all())

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    return json_response([user])

def products(request):
    return json_response(Product.objects.all())

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return json_response([product])

def orders(request):
    return json_response(Order.objects.all())

def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    return json_response([order])

def productsnapshots(request):
    return json_response(ProductSnapshot.objects.all())

def productsnapshot(request, productsnapshot_id):
    productsnapshot = ProductSnapshot.objects.get(pk=productsnapshot_id)
    return json_response([productsnapshot])

def categories(request):
    return json_response(Category.objects.all())

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return json_response([category])

def conditions(request):
    return json_response(Condition.objects.all())

def condition(request, condition_id):
    condition = Condition.objects.get(pk = condition_id)
    return json_response([condition])

def user_orders(request, buyer_id):
    return json_response(Order.objects.all().filter(buyer = buyer_id))

def category_products(request, category_id):
    return json_response(Product.objects.all().filter(category = category_id))

def json_response(list_of_objects):
    data = serializers.serialize("json", list_of_objects)
    return JsonResponse(data, safe = False)
