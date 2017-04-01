from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from urllib.error import URLError, HTTPError
import urllib.request
import json


# Create your views here.
def index(request):
    helloMsg = "Experience Home! API Version: 1"
    return render(request, 'isa_exp_app/index.html', {'helloMsg' : helloMsg})

def search_results(request):
    # Get all the products
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products')

    # Verify that no error occurred here
    if resp["response"] == "failure":
        return getJsonResponseForLayerOneError(resp)

    results = resp["data"]

    # Hydrate the associated seller info, category info, and condition info
    result = hydrateAssociatedModels(results, [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])
    
    # Return the appropriate JsonRespose (either error or success)
    if result != None:
        return result
    else:
        return getJsonResponseForResults(results)

def hot_items(request):
    # Get all the products
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products')

    # Verify that no error occurred here
    if resp["response"] == "failure":
        return getJsonResponseForLayerOneError(resp)

    # Grab the two products with the lowest stock values as our 'hot items' for now
    results = resp["data"]
    hotitems = sorted(results, key=lambda x: x["fields"]["stock"])
    if (len(hotitems) > 1):
        results = hotitems[:2]
    else:
        results = hotitems

    # Hydrate the associated seller info, category info, and condition info
    result = hydrateAssociatedModels(results, [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])
    
    # Return the appropriate JsonRespose (either error or success)
    if result != None:
        return result
    else:
        return getJsonResponseForResults(results)

def product_details(request, product_id):
    # Get the specific product we care about
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products/' + product_id)

    # Verify that no error occurred here
    if resp["response"] == "failure":
        return getJsonResponseForLayerOneError(resp)

    results = resp["data"]

    # Hydrate the associated seller info, category info, and condition info
    result = hydrateAssociatedModels(results, [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])

    # Return the appropriate JsonResponse (either error or success)
    if result != None:
        return result
    else:
        return getJsonResponseForResults(results)

def user_profile(request, user_id):
    # Get the specific user we care about
    userResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/' + user_id)

    # Get the purchased orders for this User
    purchasedResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/' + user_id + '/purchased')

    # Get the sold orders for this User
    soldResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/' + user_id + '/sold')

    # Get the products which this user is currently selling
    sellingResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/' + user_id + '/selling')

    # Verify that no errors have occurred thus far
    for response in [userResponse, purchasedResponse, soldResponse, sellingResponse]:
        if response["response"] == "failure":
            return getJsonResponseForLayerOneError(response)

    # Begin Building the result
    results = userResponse["data"]

    # Hydrate the 'purchases' and 'sold' orders and append them to the result
    for orderInfo in [[purchasedResponse, "purchases"], [soldResponse, "sold"]]:
        # Hydrate the seller info, buyer info, and product_snapshot info for each order
        orderInfoResult = hydrateAssociatedModels(orderInfo[0]["data"], [["users/", "seller"], ["users/", "buyer"], ["productsnapshots/", "product_snapshot"]])

        # Verify that no error occurred here
        if orderInfoResult != None:
            return orderInfoResult

        # Hydrate the product snapshots inside the orders
        for order in orderInfo[0]["data"]:
            temp = hydrateAssociatedModels([order["fields"]["product_snapshot"]], [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])
            # Return if we hit an error
            if temp != None:
                return temp

        
        results[0][orderInfo[1]] = orderInfo[0]["data"]

    # Hydrate the seller info, category info, and condition info for each product
    # Then append 'currently_selling' to the result
    sellingResult = hydrateAssociatedModels(sellingResponse["data"], [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])

    # Verify that no error occurred here
    if sellingResult != None:
        return sellingResult

    # Append 'selling' products to the result
    results[0]["currently_selling"] = sellingResponse["data"]

    # Return final result
    return getJsonResponseForResults(results)

def createaccount(request):
    signupResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/', "POST", urllib.parse.urlencode(request.POST).encode('utf-8'))
    return JsonResponse(signupResponse)

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

def getJsonResponseForResults(results):
    return JsonResponse({"response" : "success", "count" : str(len(results)), "data" : results})

def getJsonResponseForLayerOneError(resp):
    return JsonResponse({"response" : "failure", "error" : {"msg" : resp["error"]["msg"]}})

'''
PARAMS: 'productList' is a list of products returned from the Layer 2 api
PARAMS: 'endpoint' is the endpoint of the associated model info (ex. 'categories/' or 'users/')
PARAMS: 'key' is the key in the product fields whose value is the id of the associated model
RETURN: None on success and JsonResponse on Failure
SIDE EFFECTS: Value at product["fields"][key] goes to product["fields"][key+"_id"] AND
product["fields"][key] now refers to associated model's fields
'''
def hydrateAssociatedModelInfo(products, endpoint, key):
    for prod in products:
        resp = getJsonReponseObject("http://models-api:8000/isa_models/api/v1/" + endpoint + str(prod["fields"][key]))
        if resp["response"] == "success":
            prod["fields"][key + "_id"] = prod["fields"][key]
            prod["fields"][key] = resp["data"][0]
        else:
            return getJsonResponseForLayerOneError(resp)

    return None
'''
PARAMS: 'results' is a list of products returned from the Layer 2 api
PARAMS: 'associatedModelParams' is a list of lists, where the interiors lists have size 2 specifying
        the endpoint of the associated model info and the key whose value is the id of the associated model
        Example: associatedModelParams = [["users/", "seller"], ["categories/", "category"]]
RETURN: None on success and JsonResponse on Failure
SIDE EFFECTS: Calls 'hydrateAssociatedModelInfo' on results for each pair of model params
'''
def hydrateAssociatedModels(results, associatedModelParams):
    for modelParams in associatedModelParams:
        result = hydrateAssociatedModelInfo(results, modelParams[0], modelParams[1]);
        if result != None:
            return result

    return None
