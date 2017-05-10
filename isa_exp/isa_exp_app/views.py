from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from urllib.error import URLError, HTTPError
import urllib.request
import json
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

# Create your views here.
def index(request):
    helloMsg = "Experience Home! API Version: 1"
    return render(request, 'isa_exp_app/index.html', {'helloMsg' : helloMsg})

def search_results(request):
    search_query = request.POST['search_query']
    es = Elasticsearch(['es'])

    try:
        search_results = es.search(index='listing_index', body={'query': {'query_string': {'query' : search_query}}, 'size': 10})
    except:
        # This will occur if a search is executed before the listing_index has been created
        return JsonResponse({"response" : "failure", "error" : {"msg" : "Search index not yet created (create a new listing for this to happen)."}})

    returned_items = search_results['hits']['hits']
    hydrated_results = []
    for item in returned_items:
        resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products/' + str(item['_source']['id']))

        # Verify that no error occurred here
        if resp["response"] == "success":
            # Hydrate the associated seller info, category info, and condition info
            # And append the hyrdated_result to our hyrdrated results list
            result = resp["data"]
            error = hydrateAssociatedModels(result, [["users/", "seller"], ["categories/", "category"], ["conditions/", "condition"]])
            if error == None:
                hydrated_results.append(result[0])

    return getJsonResponseForResults(hydrated_results)

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

def new_posts(request):
    # Get all the products
    resp = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products')

    # Verify that no error occurred here
    if resp["response"] == "failure":
        return getJsonResponseForLayerOneError(resp)

    # Grab the four products (in stock) with the newest ids
    results = resp["data"]
    new_posts = filter(lambda product: (product["fields"]["stock"] > 0) and (product["fields"]["sold"] == False), results)
    new_posts = sorted(new_posts, key=lambda product: product["pk"], reverse=True)
    if (len(new_posts) > 3):
        results = new_posts[:4]
    else:
        results = new_posts

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

    # Record this product view in Kafka if we know the user_id
    if "user_id" in request.GET:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        productView = { 'user_id' : request.GET["user_id"], 'product_id' : product_id }
        producer.send('new-recommendations-topic', json.dumps(productView).encode('utf-8'))

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

def login(request):
    loginResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/login/', "POST", urllib.parse.urlencode(request.POST).encode('utf-8'))
    return JsonResponse(loginResponse)

def createlisting(request):
    if request.method == "GET": # Return the data needed by the create listing experience
        # STEP 1: Get all categories
        categoriesResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/categories')

        # Verify that no error occurred here
        if categoriesResponse["response"] == "failure":
            return getJsonResponseForLayerOneError(categoriesResponse)

        categories = categoriesResponse["data"]

        # STEP 2: Get all conditions
        conditionsResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/conditions')

        # Verify that no error occurred here
        if conditionsResponse["response"] == "failure":
            return getJsonResponseForLayerOneError(conditionsResponse)

        conditions = conditionsResponse["data"]

        # STEP 3: Combine them and return the result
        results = {}
        results["conditions"] = conditions
        results["categories"] = categories
        return getJsonResponseForResults(results)

    else: # POST
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        listingResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products/', "POST", urllib.parse.urlencode(request.POST).encode('utf-8'))
        if listingResponse['response'] == 'success':
            new_listing = {'id' : listingResponse['data'][0]['pk'], 'name' : listingResponse['data'][0]['fields']['name'], 'description' : listingResponse['data'][0]['fields']['description']}
            producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))
        return JsonResponse(listingResponse)

def editlisting(request, id):
    if request.method == "POST":
        listingResponse = getJsonReponseObject('http://models-api:8000/isa_models/api/v1/products/' + id + '/', "POST", urllib.parse.urlencode(request.POST).encode('utf-8'))
        if listingResponse['response'] == 'success':
            # First, remove the old Elastic Search Entry
            es = Elasticsearch(['es'])
            es.delete(index='listing_index', id=id, doc_type='listing', refresh=True)

            # Second, add the new entry into Kafka\
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            new_listing = {'id' : listingResponse['data'][0]['pk'], 'name' : listingResponse['data'][0]['fields']['name'], 'description' : listingResponse['data'][0]['fields']['description']}
            producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))

        return JsonResponse(listingResponse)

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
