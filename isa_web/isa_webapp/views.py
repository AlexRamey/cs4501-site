from .forms import CreateAccountForm, LoginForm, CreateListingForm
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from urllib.error import URLError, HTTPError
import urllib.request
import urllib
import json
import datetime
from .decorators import login_required

def base(request):
    context = getInitialContext(request)

    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/hotitems')

    # TODO: Handle if resp["response"] == "failure"

    context['hot_items'] = resp["data"]

    return render(request, 'isa_webapp/base.html', context)

def searchproduct(request):
    context = getInitialContext(request)

    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/searchresults')

    # TODO: Handle if resp["response"] == "failure"

    context['response'] = resp # TODO: this needs to be more granular

    return render(request, 'isa_webapp/search_product.html', context)

def productdetails(request, id):
    context = getInitialContext(request)

    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/productdetails/' +id+ '/')

    # TODO: Handle if resp["response"] == "failure"

    context['response'] = resp # TODO: this needs to be more granular

    return render(request, 'isa_webapp/product_details.html', context)

@login_required
def userprofile(request):
    context = getInitialContext(request)

    userid = context["auth_id"]

    if userid == None:
        return render()

    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/userprofile/' + userid +'/')

    if resp["response"] == "success":
        if len(resp['data']) == 1:
            context["fname"] = resp['data'][0]['fields']['first_name']
            context["lname"] = resp['data'][0]['fields']['last_name']
            context["email"] = resp['data'][0]['fields']['email']
            context["phone"] = resp['data'][0]['fields']['phone_number']
            context["brating"] = resp['data'][0]['fields']['buyer_rating']
            context["srating"] = resp['data'][0]['fields']['seller_rating']

            context["purchase"] = resp['data'][0]['purchases']
            context["purchasenum"] = len(resp['data'][0]['purchases'])
            context["sold"] = resp['data'][0]['sold']
            context["soldnum"] = len(resp['data'][0]['sold'])
            context["selling"] = resp['data'][0]['currently_selling']
            context["selling_num"] = len(resp['data'][0]['currently_selling'])
    else:
        context["error"] = resp["error"]["msg"]

    return render(request, 'isa_webapp/user_profile.html', context)

def createaccount(request):
    context = getInitialContext(request)

    if request.method == "POST":
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/createaccount/', "POST", urllib.parse.urlencode(form.cleaned_data).encode('utf-8'))
            if resp["response"] == "success":
                return getRedirectResponseThatSetsAuthCookies(resp, reverse('base'))
            else:
                context["error"] = resp["error"]["msg"]
    
    else: # GET
        form = CreateAccountForm()

    
    context["form"] = form
    return render(request, 'isa_webapp/create_account.html', context)

def login(request):
    context = getInitialContext(request)
    context["next"] = "/isa_web/login/"
    if "next" in request.GET:
        context["next"] +=  "?next=" + request.GET["next"]

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/login/', "POST", urllib.parse.urlencode(form.cleaned_data).encode('utf-8'))
            if resp["response"] == "success":
                next_path = request.GET.get("next", reverse('base'))
                return getRedirectResponseThatSetsAuthCookies(resp, next_path)
            else:
                context["error"] = resp["error"]["msg"]

    else: # GET
        form = LoginForm()

    context["form"] = form
    return render(request, 'isa_webapp/login.html', context)

def logout(request):
    if request.method == "POST":
        response = HttpResponseRedirect(reverse('base'))
        response.delete_cookie("auth")
        response.delete_cookie("auth_name")
        return response
    else: # GET
        context = getInitialContext(request)
        return render(request, 'isa_webapp/logout.html', context)

@login_required
def createlisting(request):
    context = getInitialContext(request)
    resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/createlisting')

    if resp["response"] == "failure":
        return HttpResponseRedirect(reverse('base'))

    categories = resp["data"]["categories"]
    categories = map((lambda category: (category["pk"], category["fields"]["name"])), categories)
    conditions = resp["data"]["conditions"]
    conditions = map((lambda condition: (condition["pk"], condition["fields"]["name"])), conditions)

    if request.method == "POST":
        form = CreateListingForm(categories, conditions, context["auth"], request.POST)

        if form.is_valid():
            resp = getJsonReponseObject('http://exp-api:8000/isa_experience/api/v1/createlisting/', "POST", urllib.parse.urlencode(form.cleaned_data).encode('utf-8'))
            if resp["response"] == "success":
                # TODO: Maybe go to a success page here
                # BTW: A user's listings should appear on their profile page
                return HttpResponseRedirect(reverse('base'))
            else:
                context["error"] = resp["error"]["msg"]

    else: # GET
        form = CreateListingForm(categories, conditions, context["auth"])

    context["form"] = form
    return render(request, 'isa_webapp/create_listing.html', context)

# HELPER METHODS
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

def getInitialContext(request):
    context = {}
    context["auth"] = request.COOKIES.get('auth')
    context["auth_name"] = request.COOKIES.get('auth_name')
    context["auth_id"] = request.COOKIES.get('auth_id')
    return context

def getRedirectResponseThatSetsAuthCookies(successResponseWithAuth, redirectPath):
    response = HttpResponseRedirect(redirectPath)
    expiration = datetime.datetime.now() + datetime.timedelta(weeks=1)
    response.set_cookie("auth", value=successResponseWithAuth["data"][0]["auth"], expires=expiration, httponly=True)
    response.set_cookie("auth_name", value=successResponseWithAuth["data"][0]["fields"]["first_name"], expires=expiration, httponly=True)
    response.set_cookie("auth_id", value=successResponseWithAuth["data"][0]["pk"], expires=expiration, httponly=True)
    return response
