from django.shortcuts import render

from django.http import JsonResponse

from isa_models.models import User, Category, Condition, Product, ProductSnapshot, Order
# Create your views here.

def index(request):
    return render(request, 'isa_site/index.html')

def users(request):
    users = User.objects.all()
    users_list = list(users)
    return JsonResponse(users_list, safe = False)

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    return JsonResponse(user, safe = False)

def products(request):
    products = Product.objects.all()
    products_list = list(products)
    return JsonResponse(products_list, safe = False)

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return JsonResponse(product, safe = False)

def orders(request):
    orders = Order.objects.all()
    orders_list = list(orders)
    return JsonResponse(orders_list, safe = False)

def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    return JsonResponse(order, safe = False)

def productsnapshots(request):
    productsnapshots = ProductSnapshot.objects.all()
    productsnapshots_list = list(productsnapshots)
    return JsonResponse(productsnapshots_list, safe = False)

def productsnapshot(request, productsnapshot_id):
    productsnapshot = ProductSnapshot.objects.get(pk=productsnapshot_id)
    return JsonResponse(productsnapshot, safe = False)

def categories(request):
    categories = Category.objects.all()
    categories_list = list(categories)
    return JsonResponse(categories_list, safe = False)

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return JsonResponse(category, safe = False)

def conditions(request):
    conditions = Condition.objects.all()
    conditions_list = list(conditions)
    return JsonResponse(conditions_list, safe = False)

def condition(request, condition_id):
    condition = Condition.objects.get(pk = condition_id)
    return JsonResponse(condition, safe = False)

def user_orders(request, buyer_id):
    orders = Order.objects.filter(buyer = buyer_id)
    orders_list = list(orders)
    return JsonResponse(orders_list, safe = False)

def category_products(request, category_id):
    products = Product.filter(category = category_id)
    products_list = list(products)
    return JsonResponse(products_list, safe = False)
