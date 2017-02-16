# cs4501-site
cs4501 project

# Admin Credentials
Username: 'root'
Password: 'rootpassword'

# Models API:
- `/isa_models/`
	- **GET**: Models Home Page
	
- `/isa_models/users/`
	- **GET**: Returns All Users
	- **POST**: Creates a New User

- `/isa_models/users/:userId/`
	- **GET**: Returns the User with Id equal to :userId
	- **POST**: Updates the User with Id equal to :userId with the POST params **(NOT YET IMPLEMENTED)**

- `/isa_models/products/`
	- **GET**: Returns All Products
	- **POST**: Creates a New Product

- `/isa_models/products/:productId/`
	- **GET**: Returns the Product with Id equal to :productId
	- **POST**: Updates the Product with Id equal to :productId with the POST params **(NOT YET IMPLEMENTED)**
	
- `/isa_models/orders/`
	- **GET**: Returns All Orders
	- **POST**: Creates a New Order

- `/isa_models/orders/:orderId/`
	- **GET**: Returns the Order with Id equal to :orderId
	- **POST**: Updates the Order with Id equal to :orderId with the POST params **(NOT YET IMPLEMENTED)**
	
- `/isa_models/productsnapshots/`
	- **GET**: Returns All ProductSnapshots
	- **POST**: Creates a New ProductSnapshot

- `/isa_models/productsnapshots/:productSnapshotId/`
	- **GET**: Returns the ProductSnapshot with Id equal to :productSnapshotId
	- **POST**: Updates the ProductSnapshot with Id equal to :productSnapshotId with the POST params **(NOT YET IMPLEMENTED)**
	
- `/isa_models/conditions/`
	- **GET**: Returns All Conditions
	- **POST**: Creates a New Condition

- `/isa_models/conditions/:conditionId/`
	- **GET**: Returns the Condition with Id equal to :conditionId
	- **POST**: Updates the Condition with Id equal to :conditionId with the POST params

- `/isa_models/categories/`
	- **GET**: Returns All Categories
	- **POST**: Creates a New Category

- `/isa_models/categories/:categoryId/`
	- **GET**: Returns the Category with Id equal to :categoryId
	- **POST**: Updates the Category with Id equal to :categoryId with the POST params
