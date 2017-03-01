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

- `/isa_experience/api/v1/hotitems/`
	- **GET**: Current Implementation Returns Two Products With Lowest Stock along With Associated Seller Info
	
- `/isa_experience/api/v1/searchresults/`
	- **GET**: Returns All Products (For Now)

## Response Format:
### HotItems Success Sample Response:
* Required: `response`, `data`, and `count`
```json
{
	"response" : "success",
	"count" : 2
	"data" : [
			{ 
				"model": "isa_models.product", 
				"fields": 
						{
							"sold": false,
							"name": "Pink Guitar",
							"condition": 2,
							"stock": 1,
							"category": 1,
							"price": 300.0,
							"seller":
									{
										"last_name": "buffet",
										"email": "jimmybuffet@coralreefers.edu",
										"ship_address": "101 Island Way",
										"first_name": "jimmy",
										"ship_postal_code": "22402",
										"password": "password",
										"ship_city": "Miami",
										"phone_number": "1-098-765-4321",
										"buyer_rating": 100.0,
										"seller_rating": 100.0,
										"ship_country": "USA"
									},
							"seller_id": 2,
							"description": "From my live performance in Key Largo"
						}, 
				"pk": 1
			},
			{
				"model": "isa_models.product", 
				"fields": 
						{
							"sold": false, 
							"name": "Apple Watch", 
							"condition": 2, 
							"stock": 1, 
							"category": 4, 
							"price": 50.0, 
							"seller": 
									{
										"last_name": "springsteen",
										"email": "brucespringsteen@boardwalk.org",
										"ship_address": "151 pike street",
										"first_name": "bruce",
										"ship_postal_code": "56789",
										"password": "password",
										"ship_city": "trenton",
										"phone_number": "4-321-109-8765",
										"buyer_rating": 80.0,
										"seller_rating": 100.0,
										"ship_country": "USA"
									},
							"seller_id": 3,
							"description": "Barely used!"
						},
				"pk": 2
			}
			
		 ]
}
```

### SearchResults Success Sample Response:
* Required: `response`, `data`, and `count`
```json
{
	"response": "success",
	"count": "4", 
	"data": 
		[
			{
				"model": "isa_models.product",
				"fields": 
						{
							"price": 300.0,
							"condition": 2,
							"stock": 1,
							"seller": 2,
							"category": 1,
							"description": "From my live performance in Key Largo",
							"name": "Pink Guitar",
							"sold": false
						},
				"pk": 1
			},
			{
				"model": "isa_models.product", 
				"fields": 
						{
							"price": 50.0,
							"condition": 2,
							"stock": 1,
							"seller": 3,
							"category": 4,
							"description": "Barely used!",
							"name": "Apple Watch",
							"sold": false
						},
				"pk": 2
			},
			{
				"model": "isa_models.product",
				"fields":
						{
							"price": 8.0,
							"condition": 1,
							"stock": 50,
							"seller": 1,
							"category": 2,
							"description": "The Dude Abides",
							"name": "The Big Lebowski DVD",
							"sold": false
						},
				"pk": 3
			},
			{
				"model": "isa_models.product",
				"fields": 
						{
							"price": 42.0,
							"condition": 2,
							"stock": 5,
							"seller": 1,
							"category": 1,
							"description": "fruit",
							"name": "banana",
							"sold": false
						},
				"pk": 4
			}
		]
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
