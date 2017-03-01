# cs4501-site
cs4501 project

# Models API:

## Endpoints:
- `/isa_models/api/v1/`
	- **GET**: Models Home Page
	
- `/isa_models/api/v1/users/`
	- **GET**: Returns All Users
	- **POST**: Creates a New User

- `/isa_models/api/v1/users/:userId/`
	- **GET**: Returns the User with Id equal to :userId
	- **POST**: Updates the User with Id equal to :userId with the POST params
	- **DELETE**: Deletes the User with Id equal to :userId

- `/isa_models/api/v1/products/`
	- **GET**: Returns All Products
	- **POST**: Creates a New Product

- `/isa_models/api/v1/products/:productId/`
	- **GET**: Returns the Product with Id equal to :productId
	- **POST**: Updates the Product with Id equal to :productId with the POST params
	- **DELETE**: Deletes the Product with Id equal to :productId
	
- `/isa_models/api/v1/orders/`
	- **GET**: Returns All Orders
	- **POST**: Creates a New Order

- `/isa_models/api/v1/orders/:orderId/`
	- **GET**: Returns the Order with Id equal to :orderId
	- **POST**: Updates the Order with Id equal to :orderId with the POST params
	- **DELETE**: Deletes the Order with Id equal to :orderId
	
- `/isa_models/api/v1/productsnapshots/`
	- **GET**: Returns All ProductSnapshots
	- **POST**: Creates a New ProductSnapshot

- `/isa_models/api/v1/productsnapshots/:productSnapshotId/`
	- **GET**: Returns the ProductSnapshot with Id equal to :productSnapshotId
	- **POST**: Updates the ProductSnapshot with Id equal to :productSnapshotId with the POST params
	- **DELETE**: Deletes the ProductSnapshot with Id equal to :productSnapshotId
	
- `/isa_models/api/v1/conditions/`
	- **GET**: Returns All Conditions
	- **POST**: Creates a New Condition

- `/isa_models/api/v1/conditions/:conditionId/`
	- **GET**: Returns the Condition with Id equal to :conditionId
	- **POST**: Updates the Condition with Id equal to :conditionId with the POST params
	- **DELETE**: Deletes the Condition with Id equal to :condition

- `/isa_models/api/v1/categories/`
	- **GET**: Returns All Categories
	- **POST**: Creates a New Category

- `/isa_models/api/v1/categories/:categoryId/`
	- **GET**: Returns the Category with Id equal to :categoryId
	- **POST**: Updates the Category with Id equal to :categoryId with the POST params
	- **DELETE**: Deletes the Category with Id equal to :categoryId
	
- `/isa_models/api/v1/users/:userId/purchased/`
	- **GET**: Returns a List of Orders where User with Id equal to :userId is the BUYER

- `/isa_models/api/v1/users/1/sold/`
	- **GET**: Returns a List of Orders where User with Id equal to :userId is the SELLER
	
- `/isa_models/api/v1/users/1/selling/`
	- **GET**: Returns a List of Products which are currently being sold by User with Id equal to :userId
	
## Response Format:

The response is always a JSON Dictionary with a top-level `response` key whose value is either `success` or `failure`.

### On Success:
* Required: `response` and `data`
* Optional: `msg`
```json
{
	"response" : "success", 
	"data" : [
			{ . . .},
			{ . . .},
			{ . . .}
		 ],
	"msg" : "This is a message"
}
```

### On Failure:
* Required: `response` and `error` with `msg`
* Optional: `debug`
```json
{
	"response" : "failure", 
	"error" : {
			"msg" : "Entity Does Not Exist.",
			"debug" : { . . . }
		  }
}
```

# Experience Layer API:

## Endpoints:
### These all return fully-hydrated models, meaning that if one requested model has a foreign key to another model, the requested model will come back with the complete other model inside of it (totally fleshed out)

- `/isa_experience/api/v1/hotitems/`
	- **GET**: Current Implementation Returns the Two Products with the Lowest Stock
	
- `/isa_experience/api/v1/searchresults/`
	- **GET**: Returns All Products (For Now)
	
- `/isa_experience/api/v1/productdetails/:productId/`
	- **GET**: Returns the Product with Id equal to :productId
	
- `/isa_experience/api/v1/userprofile/:userId/`
	- **GET**: Returns the Profile for the User with Id equal to :userId

## Response Format:
### hotitems Success Sample Response:
* Required: `response`, `data`, and `count`
```json
{
    "data":[
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"jimmy",
                        "seller_rating":100,
                        "buyer_rating":100,
                        "password":"password",
                        "last_name":"buffet",
                        "ship_address":"101 Island Way",
                        "email":"jimmybuffet@coralreefers.edu",
                        "phone_number":"1-098-765-4321",
                        "ship_country":"USA",
                        "ship_city":"Miami",
                        "ship_postal_code":"22402"
                    },
                    "model":"isa_models.user",
                    "pk":2
                },
                "category_id":1,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"Pink Guitar",
                "price":300,
                "seller_id":2,
                "sold":false,
                "stock":1,
                "category":{
                    "fields":{
                        "name":"Music"
                    },
                    "model":"isa_models.category",
                    "pk":1
                },
                "condition_id":2,
                "description":"From my live performance in Key Largo"
            },
            "model":"isa_models.product",
            "pk":1
        },
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"bruce",
                        "seller_rating":100,
                        "buyer_rating":80,
                        "password":"password",
                        "last_name":"springsteen",
                        "ship_address":"151 pike street",
                        "email":"brucespringsteen@boardwalk.org",
                        "phone_number":"4-321-109-8765",
                        "ship_country":"USA",
                        "ship_city":"trenton",
                        "ship_postal_code":"56789"
                    },
                    "model":"isa_models.user",
                    "pk":3
                },
                "category_id":4,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"Apple Watch",
                "price":50,
                "seller_id":3,
                "sold":false,
                "stock":1,
                "category":{
                    "fields":{
                        "name":"Devices"
                    },
                    "model":"isa_models.category",
                    "pk":4
                },
                "condition_id":2,
                "description":"Barely used!"
            },
            "model":"isa_models.product",
            "pk":2
        }
    ],
    "response":"success",
    "count":"2"
}
```

### searchresults Success Sample Response:
* Required: `response`, `data`, and `count`
```json	
{
    "data":[
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"jimmy",
                        "seller_rating":100,
                        "buyer_rating":100,
                        "password":"password",
                        "last_name":"buffet",
                        "ship_address":"101 Island Way",
                        "email":"jimmybuffet@coralreefers.edu",
                        "phone_number":"1-098-765-4321",
                        "ship_country":"USA",
                        "ship_city":"Miami",
                        "ship_postal_code":"22402"
                    },
                    "model":"isa_models.user",
                    "pk":2
                },
                "category_id":1,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"Pink Guitar",
                "price":300,
                "seller_id":2,
                "sold":false,
                "stock":1,
                "category":{
                    "fields":{
                        "name":"Music"
                    },
                    "model":"isa_models.category",
                    "pk":1
                },
                "condition_id":2,
                "description":"From my live performance in Key Largo"
            },
            "model":"isa_models.product",
            "pk":1
        },
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"bruce",
                        "seller_rating":100,
                        "buyer_rating":80,
                        "password":"password",
                        "last_name":"springsteen",
                        "ship_address":"151 pike street",
                        "email":"brucespringsteen@boardwalk.org",
                        "phone_number":"4-321-109-8765",
                        "ship_country":"USA",
                        "ship_city":"trenton",
                        "ship_postal_code":"56789"
                    },
                    "model":"isa_models.user",
                    "pk":3
                },
                "category_id":4,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"Apple Watch",
                "price":50,
                "seller_id":3,
                "sold":false,
                "stock":1,
                "category":{
                    "fields":{
                        "name":"Devices"
                    },
                    "model":"isa_models.category",
                    "pk":4
                },
                "condition_id":2,
                "description":"Barely used!"
            },
            "model":"isa_models.product",
            "pk":2
        },
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"lamar",
                        "seller_rating":100,
                        "buyer_rating":100,
                        "password":"password",
                        "last_name":"smith",
                        "ship_address":"24 Sunset Lane",
                        "email":"lamar@beaches.edu",
                        "phone_number":"1-234-567-8910",
                        "ship_country":"USA",
                        "ship_city":"Key Largo",
                        "ship_postal_code":"45678"
                    },
                    "model":"isa_models.user",
                    "pk":1
                },
                "category_id":2,
                "condition":{
                    "fields":{
                        "name":"New"
                    },
                    "model":"isa_models.condition",
                    "pk":1
                },
                "name":"The Big Lebowski DVD",
                "price":8,
                "seller_id":1,
                "sold":false,
                "stock":50,
                "category":{
                    "fields":{
                        "name":"Movies"
                    },
                    "model":"isa_models.category",
                    "pk":2
                },
                "condition_id":1,
                "description":"The Dude Abides"
            },
            "model":"isa_models.product",
            "pk":3
        },
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"lamar",
                        "seller_rating":100,
                        "buyer_rating":100,
                        "password":"password",
                        "last_name":"smith",
                        "ship_address":"24 Sunset Lane",
                        "email":"lamar@beaches.edu",
                        "phone_number":"1-234-567-8910",
                        "ship_country":"USA",
                        "ship_city":"Key Largo",
                        "ship_postal_code":"45678"
                    },
                    "model":"isa_models.user",
                    "pk":1
                },
                "category_id":1,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"banana",
                "price":42,
                "seller_id":1,
                "sold":false,
                "stock":5,
                "category":{
                    "fields":{
                        "name":"Music"
                    },
                    "model":"isa_models.category",
                    "pk":1
                },
                "condition_id":2,
                "description":"fruit"
            },
            "model":"isa_models.product",
            "pk":4
        }
    ],
    "response":"success",
    "count":"4"
}
```
### productdetails Success Sample Response:
* Required: `response`, `data`, and `count`
```json
{
    "data":[
        {
            "fields":{
                "seller":{
                    "fields":{
                        "first_name":"bruce",
                        "seller_rating":100,
                        "buyer_rating":80,
                        "password":"password",
                        "last_name":"springsteen",
                        "ship_address":"151 pike street",
                        "email":"brucespringsteen@boardwalk.org",
                        "phone_number":"4-321-109-8765",
                        "ship_country":"USA",
                        "ship_city":"trenton",
                        "ship_postal_code":"56789"
                    },
                    "model":"isa_models.user",
                    "pk":3
                },
                "category_id":4,
                "condition":{
                    "fields":{
                        "name":"Good"
                    },
                    "model":"isa_models.condition",
                    "pk":2
                },
                "name":"Apple Watch",
                "price":50,
                "seller_id":3,
                "sold":false,
                "stock":1,
                "category":{
                    "fields":{
                        "name":"Devices"
                    },
                    "model":"isa_models.category",
                    "pk":4
                },
                "condition_id":2,
                "description":"Barely used!"
            },
            "model":"isa_models.product",
            "pk":2
        }
    ],
    "response":"success",
    "count":"1"
}
```
### userprofile Success Sample Response:
* Required: `response`, `data`, and `count`
```json
{
    "data":[
        {
            "model":"isa_models.user",
            "currently_selling":[
                {
                    "fields":{
                        "seller":{
                            "fields":{
                                "first_name":"jimmy",
                                "seller_rating":100,
                                "buyer_rating":100,
                                "password":"password",
                                "last_name":"buffet",
                                "ship_address":"101 Island Way",
                                "email":"jimmybuffet@coralreefers.edu",
                                "phone_number":"1-098-765-4321",
                                "ship_country":"USA",
                                "ship_city":"Miami",
                                "ship_postal_code":"22402"
                            },
                            "model":"isa_models.user",
                            "pk":2
                        },
                        "category_id":1,
                        "condition":{
                            "fields":{
                                "name":"Good"
                            },
                            "model":"isa_models.condition",
                            "pk":2
                        },
                        "name":"Pink Guitar",
                        "price":300,
                        "seller_id":2,
                        "sold":false,
                        "stock":1,
                        "category":{
                            "fields":{
                                "name":"Music"
                            },
                            "model":"isa_models.category",
                            "pk":1
                        },
                        "condition_id":2,
                        "description":"From my live performance in Key Largo"
                    },
                    "model":"isa_models.product",
                    "pk":1
                }
            ],
            "fields":{
                "first_name":"jimmy",
                "seller_rating":100,
                "buyer_rating":100,
                "password":"password",
                "last_name":"buffet",
                "ship_address":"101 Island Way",
                "email":"jimmybuffet@coralreefers.edu",
                "phone_number":"1-098-765-4321",
                "ship_country":"USA",
                "ship_city":"Miami",
                "ship_postal_code":"22402"
            },
            "sold":[
                {
                    "fields":{
                        "status":"delivered",
                        "completed":false,
                        "seller_rating":4,
                        "product_snapshot_id":1,
                        "buyer_id":1,
                        "seller_id":2,
                        "delivery_method":"ups",
                        "seller":{
                            "fields":{
                                "first_name":"jimmy",
                                "seller_rating":100,
                                "buyer_rating":100,
                                "password":"password",
                                "last_name":"buffet",
                                "ship_address":"101 Island Way",
                                "email":"jimmybuffet@coralreefers.edu",
                                "phone_number":"1-098-765-4321",
                                "ship_country":"USA",
                                "ship_city":"Miami",
                                "ship_postal_code":"22402"
                            },
                            "model":"isa_models.user",
                            "pk":2
                        },
                        "buyer_rating":5,
                        "product_snapshot":{
                            "fields":{
                                "seller":{
                                    "fields":{
                                        "first_name":"lamar",
                                        "seller_rating":100,
                                        "buyer_rating":100,
                                        "password":"password",
                                        "last_name":"smith",
                                        "ship_address":"24 Sunset Lane",
                                        "email":"lamar@beaches.edu",
                                        "phone_number":"1-234-567-8910",
                                        "ship_country":"USA",
                                        "ship_city":"Key Largo",
                                        "ship_postal_code":"45678"
                                    },
                                    "model":"isa_models.user",
                                    "pk":1
                                },
                                "condition_id":1,
                                "condition":{
                                    "fields":{
                                        "name":"New"
                                    },
                                    "model":"isa_models.condition",
                                    "pk":1
                                },
                                "name":"The Big Lebowski DVD",
                                "price":8,
                                "seller_id":1,
                                "category_id":2,
                                "category":{
                                    "fields":{
                                        "name":"Movies"
                                    },
                                    "model":"isa_models.category",
                                    "pk":2
                                },
                                "description":"The Dude Abides"
                            },
                            "model":"isa_models.productsnapshot",
                            "pk":1
                        },
                        "buyer":{
                            "fields":{
                                "first_name":"lamar",
                                "seller_rating":100,
                                "buyer_rating":100,
                                "password":"password",
                                "last_name":"smith",
                                "ship_address":"24 Sunset Lane",
                                "email":"lamar@beaches.edu",
                                "phone_number":"1-234-567-8910",
                                "ship_country":"USA",
                                "ship_city":"Key Largo",
                                "ship_postal_code":"45678"
                            },
                            "model":"isa_models.user",
                            "pk":1
                        },
                        "order_date":"2017-01-15",
                        "tracking_number":"564"
                    },
                    "model":"isa_models.order",
                    "pk":3
                }
            ],
            "purchases":[
                {
                    "fields":{
                        "status":"In Route",
                        "completed":false,
                        "seller_rating":5,
                        "product_snapshot_id":1,
                        "buyer_id":2,
                        "seller_id":1,
                        "delivery_method":"UPS",
                        "seller":{
                            "fields":{
                                "first_name":"lamar",
                                "seller_rating":100,
                                "buyer_rating":100,
                                "password":"password",
                                "last_name":"smith",
                                "ship_address":"24 Sunset Lane",
                                "email":"lamar@beaches.edu",
                                "phone_number":"1-234-567-8910",
                                "ship_country":"USA",
                                "ship_city":"Key Largo",
                                "ship_postal_code":"45678"
                            },
                            "model":"isa_models.user",
                            "pk":1
                        },
                        "buyer_rating":5,
                        "product_snapshot":{
                            "fields":{
                                "seller":{
                                    "fields":{
                                        "first_name":"lamar",
                                        "seller_rating":100,
                                        "buyer_rating":100,
                                        "password":"password",
                                        "last_name":"smith",
                                        "ship_address":"24 Sunset Lane",
                                        "email":"lamar@beaches.edu",
                                        "phone_number":"1-234-567-8910",
                                        "ship_country":"USA",
                                        "ship_city":"Key Largo",
                                        "ship_postal_code":"45678"
                                    },
                                    "model":"isa_models.user",
                                    "pk":1
                                },
                                "condition_id":1,
                                "condition":{
                                    "fields":{
                                        "name":"New"
                                    },
                                    "model":"isa_models.condition",
                                    "pk":1
                                },
                                "name":"The Big Lebowski DVD",
                                "price":8,
                                "seller_id":1,
                                "category_id":2,
                                "category":{
                                    "fields":{
                                        "name":"Movies"
                                    },
                                    "model":"isa_models.category",
                                    "pk":2
                                },
                                "description":"The Dude Abides"
                            },
                            "model":"isa_models.productsnapshot",
                            "pk":1
                        },
                        "buyer":{
                            "fields":{
                                "first_name":"jimmy",
                                "seller_rating":100,
                                "buyer_rating":100,
                                "password":"password",
                                "last_name":"buffet",
                                "ship_address":"101 Island Way",
                                "email":"jimmybuffet@coralreefers.edu",
                                "phone_number":"1-098-765-4321",
                                "ship_country":"USA",
                                "ship_city":"Miami",
                                "ship_postal_code":"22402"
                            },
                            "model":"isa_models.user",
                            "pk":2
                        },
                        "order_date":"2017-02-14",
                        "tracking_number":"12345678910"
                    },
                    "model":"isa_models.order",
                    "pk":1
                }
            ],
            "pk":2
        }
    ],
    "response":"success",
    "count":"1"
}
```

### On Failure:
* Required: `response` and `error` with `msg`
```json
{
	"response" : "failure", 
	"error" : {
			"msg" : "Entity Does Not Exist.",
		  }
}
```
