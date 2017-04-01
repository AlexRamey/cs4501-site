from .forms import CreateAccountForm, LoginForm
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from urllib.error import URLError, HTTPError
import urllib.request
import urllib
import json
import datetime

def base(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth') 
    context["auth_name"] = request.COOKIES.get('auth_name')

    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/hotitems')
    context['hot_items'] = resp["data"]

    return render(request, 'isa_webapp/base.html', context)

def searchproduct(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')

    req = urllib.request.Request('http://exp-api:8000/isa_experience/api/v1/searchresults')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    context['response'] = resp

    return render(request, 'isa_webapp/search_product.html', context)

def productdetails(request, id):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')

    req = urllib.request.Request('http://exp-api:8000/isa_experience/api/v1/productdetails/' +id+ '/')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    context['response'] = resp

    return render(request, 'isa_webapp/product_details.html', context)

# TODO: userprofile should accept a user id as a parameter
def userprofile(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')

    response = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/userprofile/:1/')
    return render(request, 'isa_webapp/user_profile.html', context)

def createaccount(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')

    if request.method == "POST":
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/createaccount/', "POST", urllib.parse.urlencode(form.cleaned_data).encode('utf-8'))
            if resp["response"] == "success":
                # Set Cookie!
                response = HttpResponseRedirect(reverse('base'))
                expiration = datetime.datetime.now() + datetime.timedelta(weeks=1)
                response.set_cookie("auth", value=resp["data"][0]["auth"], expires=expiration, httponly=True)
                response.set_cookie("auth_name", value=resp["data"][0]["fields"]["first_name"], exipres=expiration, httponly=True)
                return response
            else:
                context["error"] = "Failed to create user :("
    
    else: # GET
        form = CreateAccountForm()

    
    context["form"] = form
    return render(request, 'isa_webapp/create_account.html', context)

def login(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/login/', "POST", urllib.parse.urlencode(form.cleaned_data).encode('utf-8'))
            if resp["response"] == "success":
                # Set Cookie!
                response = HttpResponseRedirect(reverse('base'))
                expiration = datetime.datetime.now() + datetime.timedelta(weeks=1)
                response.set_cookie("auth", value=resp["data"][0]["auth"], expires=expiration, httponly=True)
                response.set_cookie("auth_name", value=resp["data"][0]["fields"]["first_name"], expires=expiration, httponly=True)
                return response
            else:
                context["error"] = resp["error"]["msg"]

    else: # GET
        form = LoginForm()

    context["form"] = form
    return render(request, 'isa_webapp/login.html', context)

def logout(request):
    response = HttpResponseRedirect(reverse('base'))
    response.delete_cookie("auth")
    response.delete_cookie("auth_name")
    return response

def getJsonReponseObject(url, method="GET", data=None):

    req = urllib.request.Request(url, method=method, data=data)
    
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        errorMessage = "HTTP Error: " + str(e.code)
        return JsonResponse({"response" : "failure", "error" : {"msg" : errorMessage}})
    except URLError as e:
        return JsonResponse({"response" : "failure", "error" : {"msg" : str(e.args)}})


    return json.loads(resp_json)

def getJsonResponseForLayerOneError(resp):
    return JsonResponse({"response" : "failure", "error" : {"msg" : resp["error"]["msg"]}})

    return json.loads(resp_json)

