from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from urllib.error import URLError, HTTPError
import urllib.request
import json


# Create your views here.
def index(request):
    helloMsg = "Experience Home! API Version: 1"
    return render(request, 'isa_exp_app/index.html', {'helloMsg' : helloMsg})

def searchresults(request):
    # For now, just return all the products
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products')

    if resp["response"] == "success":
        count = len(resp["data"])
        return JsonResponse({"response" : "success", "count" : str(count), "data" : resp["data"]})
    else:
        return getJsonResponseForLayerOneError(resp)

def hotitems(request):
    # For now, just return two items with the lowest stock quantity
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products')

    allproducts = resp["data"]
    hotitems = sorted(allproducts, key=lambda x: x["fields"]["stock"])
    if (len(hotitems) > 1):
        results = hotitems[:2]
    else:
        results = hotitems

    # Get the associated seller info
    for result in results:
        resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/users/'+str(result["fields"]["seller"]))
        if resp["response"] == "success":
            result["fields"]["seller_id"] = result["fields"]["seller"]
            result["fields"]["seller_info"] = resp["data"][0]["fields"]
        else:
            return getJsonResponseForLayerOneError(resp)

    if resp["response"] == "success":
        count = len(results)
        return JsonResponse({"response" : "success", "count" : str(count), "data" : results})
    else:
        return getJsonResponseForLayerOneError(resp)

# HELPER METHODS
def getJsonReponseObject(url):
    req = urllib.request.Request(url)
    
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8').replace("\\", "")
    except HTTPError as e:
        errorMessage = "HTTP Error: " + str(e.code)
        return JsonResponse({"response" : "failure", "error" : {"msg" : errorMessage}})
    except URLError as e:
        return JsonResponse({"response" : "failure", "error" : {"msg" : str(e.args)}})

    return json.loads(resp_json)

def getJsonResponseForLayerOneError(resp):
    return JsonResponse({"response" : "failure", "error" : {"msg" : resp["error"]["msg"]}})