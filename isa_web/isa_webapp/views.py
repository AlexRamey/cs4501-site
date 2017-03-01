from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
from urllib.error import URLError, HTTPError
import urllib.request
import json

def base(request):
	#helloMsg = "Experience Home! API Version: 1"
	return render(request, 'isa_webapp/base.html')#, {'helloMsg' : helloMsg})

def searchproduct(request):
	# Call API from layer 2
	response = getJsonResponseObject('http://isa_experience/api/v1/searchresults')

	if response["response"] == "success":
		count = len(resp["data"])
		return JsonResponse({"response" : "success", "count" : str(count), "data" : resp["data"]})
	else:
		return getJsonResponseForLayerOneError(resp)


def getJsonResponseObject(url):
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