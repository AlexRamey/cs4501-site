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
