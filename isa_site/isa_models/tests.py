from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from isa_models.models import Category
from isa_models.models import Condition

class GetTestCategory(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()

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

    # def test_success_create_response(self):
    # 	response = self.client.post(reverse('category'), {'name' : "Food"})
    # 	response = response.json()
    # 	self.assertEquals(response['response'], 'success')
    # 	self.assertTrue(isinstance(response['data'], list))
    # 	self.assertEquals(response['data'][7]['fields']['name'], "Food")
    # 	self.assertTrue(len(response['data']) == 1)   		

    # def test_success_delete_response(self):
    # 	response = self.client.delete(reverse('category'), kwargs={'category_id': 1})
    # 	response = response.json()
    # 	self.assertEquals(response['response'], 'failure')		

    # #user_id not given in url, so error
    # def fails_invalid(self):
    #     response = self.client.get(reverse('category'))
    #     self.assertEquals(response.status_code, 404)

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down

class GetTestConditions(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()

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

class GetTestProductsnapshots(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()

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
    	response = self.client.post(reverse('productsnapshot', kwargs={'productsnapshot_id': 1}))
    	print(response)
    	self.assertEquals(response['response'], 'success')
    	self.assertTrue(isinstance(response['data'], list))
    	self.assertEquals(response['data'][0]['fields']['name'], "The Big Lebowski DVD")
    	self.assertTrue(len(response['data']) == 1)



