# cs4501-site
cs4501 project

# Admin Credentials
Username: 'root'
Password: 'rootpassword'


URLs:
Index --> Home Page
Users --> GET: lists all users
	  --> POST: adds a new user
Users/id --> GET: accesses information regarding one user
		--> POST: modifies one user
Users/id/Orders --> shows all orders from a given user
Products --> GET: lists all products
		 --> POST: adds a new product
Products/id --> GET: accesses information regarding one product
		--> POST: modifies one product
Orders --> GET: lists all orders
		 --> POST: adds a new order
Orders/id --> GET: accesses information regarding one order
		--> POST: modifies one order
Productsnapshot --> GET: lists all product snapshots
		 --> POST: adds a new product snapshots
Productsnapshot/id --> GET: accesses information regarding one product snapshots
		--> POST: modifies one product snapshots
Categories --> GET: lists all category
		 --> POST: adds a new category
Categories/id --> GET: accesses information regarding one category
		--> POST: modifies one category	
Categories/id/product --> lists all products in a specific category
Conditions --> GET: lists all conditions
		 --> POST: adds a new product conditions
Conditions/id --> GET: accesses information regarding one product conditions
		--> POST: modifies one product conditions
]