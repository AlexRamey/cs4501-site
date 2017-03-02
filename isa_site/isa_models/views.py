from django.shortcuts import render

from django.http import JsonResponse, HttpResponse

from isa_models.models import User, UserForm, Category, CategoryForm, Condition, ConditionForm, Product, ProductForm, ProductSnapshot, ProductSnapshotForm, Order, OrderForm

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json

def users(request):
    return collection_response(request, UserForm(request.POST), User.objects)

def user(request, user_id):
    result = entity_or_not_found_response(User.objects, user_id)
    if not isinstance(result, User):
        return result

    return entity_response(request, result, UserForm(request.POST, instance=result))

def products(request):
    return collection_response(request, ProductForm(request.POST), Product.objects)

def product(request, product_id):
    result = entity_or_not_found_response(Product.objects, product_id)
    if not isinstance(result, Product):
        return result

    return entity_response(request, result, ProductForm(request.POST, instance=result))

def orders(request):
    return collection_response(request, OrderForm(request.POST), Order.objects)

def order(request, order_id):
    result = entity_or_not_found_response(Order.objects, order_id)
    if not isinstance(result, Order):
        return result

    return entity_response(request, result, OrderForm(request.POST, instance=result))

def productsnapshots(request):
    return collection_response(request, ProductSnapshotForm(request.POST), ProductSnapshot.objects)
    
def productsnapshot(request, productsnapshot_id):
    result = entity_or_not_found_response(ProductSnapshot.objects, productsnapshot_id)
    if not isinstance(result, ProductSnapshot):
        return result

    return entity_response(request, result, ProductSnapshotForm(request.POST, instance=result))

def categories(request):
    return collection_response(request, CategoryForm(request.POST), Category.objects)

def category(request, category_id):
    result = entity_or_not_found_response(Category.objects, category_id)
    if not isinstance(result, Category):
        return result

    return entity_response(request, result, CategoryForm(request.POST, instance=result))

def conditions(request):
    return collection_response(request, ConditionForm(request.POST), Condition.objects)

def condition(request, condition_id):
    result = entity_or_not_found_response(Condition.objects, condition_id)
    if not isinstance(result, Condition):
        return result

    return entity_response(request, result, ConditionForm(request.POST, instance=result))

def user_purchased(request, buyer_id):
    return data_json_response(Order.objects.all().filter(buyer = buyer_id))

def user_sold(request, seller_id):
    return data_json_response(Order.objects.all().filter(seller = seller_id))

def user_selling(request, seller_id):
    return data_json_response(Product.objects.all().filter(seller = seller_id, sold = False))

def category_products(request, category_id):
    return data_json_response(Product.objects.all().filter(category = category_id))

# HELPER METHODS
def data_json_response(list_of_objects):
    data = serializers.serialize("json", list_of_objects)
    response = JsonResponse(data, safe = False)
    response.content = ("{\"response\" : \"success\", \"data\" : ").encode('utf-8') + (str(response.content[1:-1], 'utf-8').replace("\\","")).encode('utf-8') + "}".encode('utf-8')
    return response

def create_or_update_model_post_response(modelForm):
    if modelForm.is_valid():
        newModel = modelForm.save()
        return data_json_response([newModel])  
    else:
        response = HttpResponse(modelForm.errors.as_json())
        response.content = "{\"response\" : \"failure\", \"error\" : {\"msg\" : \"Invalid Parameters\", \"debug\" : ".encode('utf-8') \
                            + response.content + "}}".encode('utf-8')
        return response

def entity_or_not_found_response(querySet, primaryKey):
    try:
        entity = querySet.get(pk=primaryKey)
        return entity
    except ObjectDoesNotExist:
        return JsonResponse({"response" : "failure", "error" : {"msg" : "Entity Does Not Exist."}})

def entity_deleted_json_response(entityType):
    return JsonResponse({'response' : 'success', 'data' : [], 'msg' : entityType + ' successfully deleted.'})

def collection_response(request, modelForm, querySet):
    if request.method == "POST":
        return create_or_update_model_post_response(modelForm)  
    elif request.method == "GET":
        return data_json_response(querySet.all())
    else:
        return HttpResponse("Invalid HTTP Method (must be GET or POST).", status=404)

def entity_response(request, entity, modelForm):
    if request.method == "GET":
        return data_json_response([entity])
    elif request.method == "POST":
        return create_or_update_model_post_response(modelForm)
    elif request.method == "DELETE":
        entity.delete()
        return entity_deleted_json_response(type(entity).__name__)
    else:
        return HttpResponse("Invalid HTTP Method (must be GET, POST, or DELETE).", status=404)
