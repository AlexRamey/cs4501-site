from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from isa_models.models import User, UserForm, Authenticator, Category, CategoryForm, Condition, ConditionForm, Product, ProductForm, ProductSnapshot, ProductSnapshotForm, Order, OrderForm
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
import json
import os
import hmac
from django.conf import settings
import datetime

def users(request):
    if request.method == "POST":
        # plain_text_email = request.POST["email"]
        users = User.objects.filter(email=request.POST["email"])
        if len(users) > 0:
            return JsonResponse({'response' : 'failure', 'error' : { 'msg' : 'Someone with that email already exists.'}})
        plain_text_pswd = request.POST["password"]
        if len(plain_text_pswd) < 5:
            return JsonResponse({'response' : 'failure', 'error' : { 'msg' : 'Password too short! Must be at least 5 characters long.'}})

        mutable_post_params = request.POST.copy()
        mutable_post_params["password"] = make_password(plain_text_pswd, salt=None, hasher='pbkdf2_sha256')
        resp = create_or_update_model_post_response(UserForm(mutable_post_params))

        if (json.loads(resp.content.decode('utf-8')))["response"] == "success":
            json_object = json.loads(resp.content.decode('utf-8'))
            user_id = json_object["data"][0]["pk"]
            resp = user_auth_response(User.objects.get(pk=user_id))

        return resp
    elif request.method == "GET":
        return data_json_response(User.objects.all())
    else:
        return HttpResponse("Invalid HTTP Method (must be GET or POST).", status=404)

def user(request, user_id):
    result = entity_or_not_found_response(User.objects, user_id)
    if not isinstance(result, User):
        return result

    return entity_response(request, result, UserForm(request.POST, instance=result))

def login(request):
    if request.method == "POST":
        users = User.objects.filter(email=request.POST["email"])
        if len(users) > 0:
            users = [user for user in users if check_password(request.POST["password"], user.password)]
            if len(users) > 0:
                user = users[0]
                return user_auth_response(user)

        return JsonResponse({'response' : 'failure', 'error' : { 'msg' : 'Wrong username or password!'}})
    else:
        return HttpResponse("Invalid HTTP Method (must be POST).", status=404)

def authenticators(request):
    return data_json_response(Authenticator.objects.all())

def products(request):
    if request.method == "POST":
        authenticator = request.POST["seller"]
        today = datetime.date.today()
        one_week_ago = today - datetime.timedelta(weeks=1)
        authenticators = Authenticator.objects.filter(authenticator=authenticator).filter(date_created__range=[one_week_ago, today])
        if (len(authenticators) == 0):
            return JsonResponse({'response' : 'failure', 'error' : { 'msg' : 'Invalid credentials!'}})
        else:
            mutable_post_params = request.POST.copy()
            mutable_post_params["seller"] = str(authenticators[0].user.id)
            resp = create_or_update_model_post_response(ProductForm(mutable_post_params))
            return resp
            
    elif request.method == "GET":
        return data_json_response(Product.objects.all())
    else:
        return HttpResponse("Invalid HTTP Method (must be GET or POST).", status=404)


# IN PRODUCT, NEED TO RETURN JSON RESPONSE THAT WILL BE RUN IN RECOMMMENDATIONS.PY
# JSON WITH TWO FIELDS, user_id and recommended_products (SEE recommendations.py)

def product(request, product_id):
    result = entity_or_not_found_response(Product.objects, product_id)
    if not isinstance(result, Product):
        return result
    if request.method == "POST":
        authenticator = request.POST["seller"]
        today = datetime.date.today()
        one_week_ago = today - datetime.timedelta(weeks=1)
        authenticators = Authenticator.objects.filter(authenticator=authenticator).filter(
            date_created__range=[one_week_ago, today])
        if (len(authenticators) == 0):
            return JsonResponse({'response': 'failure', 'error': {'msg': 'Invalid credentials!'}})
        elif authenticators[0].user.id != result.seller_id:
            return JsonResponse({'response': 'failure', 'error': {'msg': 'Not allowed to edit someone else product!'}})
        else:
            mutable_post_params = request.POST.copy()
            mutable_post_params["seller"] = str(authenticators[0].user.id)
            return entity_response(request, result, ProductForm(mutable_post_params, instance=result))

    elif request.method == "GET":
        return entity_response(request, result, ProductForm(request.POST, instance=result))
    elif request.method == "DELETE":
        result.delete()
        return entity_deleted_json_response(type(result).__name__)
    else:
        return HttpResponse("Invalid HTTP Method (must be GET or POST).", status=404)

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

def user_auth_response(userObject):
    # Step 1: Create the new authenticator (verify that no collision occurs)
    authenticator = getAuthenticatorToken()
    while len(Authenticator.objects.filter(authenticator=authenticator)) > 0:
        authenticator = getAuthenticatorToken()

    Authenticator(authenticator=authenticator, user=userObject).save()

    # Step 2: Get the typical JSON response for the user object, and inject auth token
    resp = data_json_response([userObject])
    json_object = json.loads(resp.content.decode('utf-8'))
    json_object["data"][0]["auth"] = authenticator
    resp = JsonResponse(json_object)
    return resp

def getAuthenticatorToken():
    return hmac.new(
        key = settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256',
    ).hexdigest()