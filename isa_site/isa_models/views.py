from django.shortcuts import render

from django.http import JsonResponse, HttpResponse

from isa_models.models import User, UserForm, Category, Condition, Product, ProductForm, ProductSnapshot, ProductSnapshotForm, Order, OrderForm

from django.core import serializers 
import json
# Create your views here.

def index(request):
    return render(request, 'isa_models/index.html')

def users(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            newUser = userForm.save()
            return json_response([newUser])  
        else:
            return HttpResponse("Invalid Parameters: " + str(userForm.errors), status=507)   
    elif request.method == "GET":
        return json_response(User.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def user(request, user_id):
    user = User.objects.get(pk=user_id)
    return json_response([user])

def products(request):
    if request.method == "POST":
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            newProduct = productForm.save()
            return json_response([newProduct])  
        else:
            return HttpResponse("Invalid Parameters: " + str(productForm.errors), status=507)   
    elif request.method == "GET":
        return json_response(Product.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return json_response([product])

def orders(request):
    if request.method == "POST":
        orderForm = OrderForm(request.POST)
        if orderForm.is_valid():
            newOrder = orderForm.save()
            return json_response([newOrder])  
        else:
            return HttpResponse("Invalid Parameters: " + str(orderForm.errors), status=507)   
    elif request.method == "GET":
        return json_response(Order.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def order(request, order_id):
    order = Order.objects.get(pk=order_id)
    return json_response([order])

def productsnapshots(request):
    if request.method == "POST":
        productSnapshotForm = ProductSnapshotForm(request.POST)
        if productSnapshotForm.is_valid():
            newProductSnapshot = productSnapshotForm.save()
            return json_response([newProductSnapshot])  
        else:
            return HttpResponse("Invalid Parameters: " + str(productSnapshotForm.errors), status=507)   
    elif request.method == "GET":
        return json_response(ProductSnapshot.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")
    
def productsnapshot(request, productsnapshot_id):
    productsnapshot = ProductSnapshot.objects.get(pk=productsnapshot_id)
    return json_response([productsnapshot])

def categories(request):
    if request.method == "POST":
        if "name" in request.POST:
            # CREATE 
            result = Category.objects.create(name=request.POST["name"])
            return json_response([result]) 
        return HttpResponse(status=507)    
    elif request.method == "GET":
        return json_response(Category.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def category(request, category_id):
    if request.method == "POST":
        if "name" in request.POST:
            # Update
            result = Category.objects.filter(pk=category_id).update(name=request.POST["name"])
            if (result == 1):
                return json_response(Category.objects.filter(pk=category_id))
            
        return HttpResponse(status=507)
    elif request.method == "GET":    
        category = Category.objects.get(pk=category_id)
        return json_response([category])
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def conditions(request):
    if request.method == "POST":
        if "name" in request.POST:
            result = Condition.objects.create(name=request.POST["name"])
            return json_response([result]) 
        return HttpResponse(status=507)    
    elif request.method == "GET":
        return json_response(Condition.objects.all())
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def condition(request, condition_id):
    if request.method == "POST":
        if "name" in request.POST:
            # Update
            result = Condition.objects.filter(pk=condition_id).update(name=request.POST["name"])
            if (result == 1):
                return json_response(Condition.objects.filter(pk=condition_id))
            
        return HttpResponse(status=507)
    elif request.method == "GET":    
        condition = Condition.objects.get(pk = condition_id)
        return json_response([condition])
    else:
        raise Http404("Invalid HTTP Method (must be GET or POST).")

def user_orders(request, buyer_id):
    return json_response(Order.objects.all().filter(buyer = buyer_id))

def category_products(request, category_id):
    return json_response(Product.objects.all().filter(category = category_id))

def json_response(list_of_objects):
    data = serializers.serialize("json", list_of_objects)
    return JsonResponse(data, safe = False)
