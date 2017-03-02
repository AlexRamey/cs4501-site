from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from isa_models.models import Category, Condition, Order, ProductSnapshot, User, Product

class GetTestCategory(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        Category.objects.create(name="Test1")

    def test_success_response(self):
        response = self.client.get(reverse('categories')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('category', kwargs={'category_id': 1}))
        response = response.json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('category', kwargs={'category_id': 1}), {'name' : "Food"})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Food")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('categories'), {'name' : "Food"})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Food")
    	self.assertTrue(len(response['data']) == 1)   		

    def test_success_delete_response(self):
    	category1 = Category.objects.get(name="Test1")
    	response = self.client.delete(reverse('category', kwargs={'category_id': category1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')		

    # #user_id not given in url, so error
    def test_invalid_input(self):
        response = self.client.get(reverse('category', kwargs={'category_id': 1000}))
        self.assertEquals(response.status_code, 200)

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down

class GetTestConditions(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        Condition.objects.create(name="Test1")

    def test_success_response(self):
        #assumes user with id 1 is stored in db
        response = self.client.get(reverse('conditions')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('condition', kwargs={'condition_id': 1}))
        response = response.json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('condition', kwargs={'condition_id': 1}), {'name' : "Bad"})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Bad")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('conditions'), {'name' : "Really Bad"})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Really Bad")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_delete_response(self):
    	condition1 = Condition.objects.get(name="Test1")
    	response = self.client.delete(reverse('condition', kwargs={'condition_id': condition1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')	

    def test_invalid_input(self):
        response = self.client.get(reverse('condition', kwargs={'condition_id': 1000}))
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        pass #nothing to tear down

class GetTestProductsnapshots(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        User.objects.create(email="vj@virginia.edu", password="password", first_name="vj", last_name="edup", phone_number="1-987-654-3210", ship_address='123 John Street', ship_city="Cville", ship_postal_code="22903", ship_country="USA", buyer_rating=100.0, seller_rating=100.0)
        num_id = User.objects.get(first_name="vj")
        Category.objects.create(name="Test1")
        cat_id = Category.objects.get(name="Test1")
        Condition.objects.create(name="Test1")
        con_id = Condition.objects.get(name="Test1")
        ProductSnapshot.objects.create(seller=num_id, name="XYZ DVD", category=cat_id, description="NA", price=10.0, condition=con_id)

    def test_success_response(self):
        #assumes user with id 1 is stored in db
        response = self.client.get(reverse('productsnapshots')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('productsnapshot', kwargs={'productsnapshot_id': 1}))
        response = response.json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('productsnapshot', kwargs={'productsnapshot_id': 1}), {'seller' : 1, 'name' : "Other DVD", 'category' : 2, 'description' : "NA", 'price' : 10.0, 'condition' : 1})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Other DVD")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('categories'), {'seller' : 1, 'name' : "Awesome DVDs", 'category' : 2, 'description' : "newly created product snapshot", 'price' : 30.0, 'condition' : 1})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Awesome DVDs")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_delete_response(self):
    	ps1 = ProductSnapshot.objects.get(name="XYZ DVD")
    	response = self.client.delete(reverse('productsnapshot', kwargs={'productsnapshot_id': ps1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')	    	
 
    def test_invalid_input(self):
        response = self.client.get(reverse('productsnapshot', kwargs={'productsnapshot_id': 1000}))
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        pass #nothing to tear down


class GetTestOrder(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        User.objects.create(email="vj@virginia.edu", password="password", first_name="vj", last_name="edup", phone_number="1-987-654-3210", ship_address='123 John Street', ship_city="Cville", ship_postal_code="22903", ship_country="USA", buyer_rating=100.0, seller_rating=100.0)
        num_id = User.objects.get(first_name="vj")
        Category.objects.create(name="Test1")
        cat_id = Category.objects.get(name="Test1")
        Condition.objects.create(name="Test1")
        con_id = Condition.objects.get(name="Test1")
        ProductSnapshot.objects.create(seller=num_id, name="XYZ DVD", category=cat_id, description="NA", price=10.0, condition=con_id)
        ps_id = ProductSnapshot.objects.get(name="XYZ DVD")
        Order.objects.create(product_snapshot=ps_id, order_date="2017-02-14", delivery_method="FedEx", tracking_number="9876543210", status="In Virginia", seller=num_id, buyer=num_id, completed=False, buyer_rating=5, seller_rating=5)

    def test_success_response(self):
        response = self.client.get(reverse('orders')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('order', kwargs={'order_id': 1}))
        response = response.json()
        #print(response)
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('order', kwargs={'order_id': 1}), {'product_snapshot' : 1, 'order_date' : "2017-02-14", 'delivery_method' : "UPS", 'tracking_number' : "1234567890", 'status' : "Not in route", 'seller' : 1, 'buyer' : 2, 'completed' : False, 'buyer_rating' : 5, 'seller_rating' : 5}).json()
    	#response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['status'], "Not in route")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('orders'), {'product_snapshot' : 1, 'order_date' : "2017-02-14", 'delivery_method' : "FedEx", 'tracking_number' : "9876543210", 'status' : "In Virginia", 'seller' : 1, 'buyer' : 2, 'completed' : False, 'buyer_rating' : 5, 'seller_rating' : 5})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['tracking_number'], "9876543210")
    	self.assertTrue(len(response['data']) == 1)

    def test_invalid_input(self):
        response = self.client.get(reverse('order', kwargs={'order_id': 1000}))
        self.assertEquals(response.status_code, 200)    	

    def test_success_delete_response(self):
    	o1 = Order.objects.get(tracking_number="9876543210")
    	response = self.client.delete(reverse('order', kwargs={'order_id': o1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')	

    def tearDown(self):
        pass #nothing to tear down

class GetTestProduct(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        User.objects.create(email="vj@virginia.edu", password="password", first_name="vj", last_name="edup", phone_number="1-987-654-3210", ship_address='123 John Street', ship_city="Cville", ship_postal_code="22903", ship_country="USA", buyer_rating=100.0, seller_rating=100.0)
        num_id = User.objects.get(first_name="vj")
        Category.objects.create(name="Test1")
        cat_id = Category.objects.get(name="Test1")
        Condition.objects.create(name="Test1")
        con_id = Condition.objects.get(name="Test1")
        Product.objects.create(seller=num_id, name="XYZQWE DVD", description="NA", category=cat_id, price=10.0, stock=2, sold=False, condition=con_id)

    def test_success_response(self):
        response = self.client.get(reverse('products')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('product', kwargs={'product_id': 1}))
        response = response.json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('product', kwargs={'product_id': 1}), {'seller' : 2, 'name' : "Food", 'description' : "N/A", 'category' : 1, 'price' : 250.0, 'stock' : 1, 'sold' : False, 'condition' : 2})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Food")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('products'), {'seller' : 2, 'name' : "Test1Product", 'description' : "N/A", 'category' : 1, 'price' : 250.0, 'stock' : 1, 'sold' : False, 'condition' : 2})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "Test1Product")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_delete_response(self):
    	p1 = Product.objects.get(name="XYZQWE DVD")
    	response = self.client.delete(reverse('product', kwargs={'product_id': p1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')

    def test_invalid_input(self):
        response = self.client.get(reverse('product', kwargs={'product_id': 1000}))
        self.assertEquals(response.status_code, 200) 


    def tearDown(self):
        pass #nothing to tear down

class GetTestUser(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()
        User.objects.create(email="vj@virginia.edu", password="password", first_name="vj", last_name="edup", phone_number="1-987-654-3210", ship_address='123 John Street', ship_city="Cville", ship_postal_code="22903", ship_country="USA", buyer_rating=100.0, seller_rating=100.0)

    def test_success_response(self):
        response = self.client.get(reverse('users')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) != 0)

    def test_success_response_one(self):
    	# assumes first element exists from fixtures
        response = self.client.get(reverse('user', kwargs={'user_id': 1}))
        response = response.json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        self.assertTrue(len(response['data']) == 1)

    def test_success_update_response(self):
    	response = self.client.post(reverse('user', kwargs={'user_id': 1}), {'email' : "vse7fd@virginia.edu", 'password' : "password", "first_name" : "vijay", "last_name" : "edupuganti", "phone_number" : "1-503-780-6755", 'ship_address' : '24 Sunset Lane', 'ship_city' : "Key Largo", 'ship_postal_code' : "45678", 'ship_country' : "USA", 'buyer_rating' : 100.0, 'seller_rating' : 100.0})
    	response = response.json()
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['first_name'], "vijay")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_create_response(self):
    	response = self.client.post(reverse('users'), {'email' : "vij@virginia.edu", 'password' : "password", "first_name" : "vij", "last_name" : "edupg", "phone_number" : "1-503-780-6755", 'ship_address' : '24 Sunset Lane', 'ship_city' : "Key Largo", 'ship_postal_code' : "45678", 'ship_country' : "USA", 'buyer_rating' : 100.0, 'seller_rating' : 100.0})
    	response = response.json() 
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['first_name'], "vij")
    	self.assertTrue(len(response['data']) == 1)

    def test_success_delete_response(self):
    	u1 = User.objects.get(email="vj@virginia.edu")
    	response = self.client.delete(reverse('user', kwargs={'user_id': u1.id}))
    	response = response.json()
    	self.assertEquals(response['response'], 'success')

    def test_invalid_input(self):
        response = self.client.get(reverse('user', kwargs={'user_id': 1000}))
        self.assertEquals(response.status_code, 200) 
    
    def tearDown(self):
        pass #nothing to tear down