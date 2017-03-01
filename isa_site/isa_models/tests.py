from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from isa_models.models import Category

class GetTestCategory(TestCase):
    #setUp method is called before each test in this class
    fixtures = ["fixture1.json"]
    def setUp(self):
        #pass #nothing to set up
        self.client = Client()

    def test_success_response(self):
        #assumes user with id 1 is stored in db
        response = self.client.get(reverse('categories')).json()
        self.assertEquals(response['response'], 'success')
        self.assertTrue(isinstance(response['data'], list))
        #self.assertTrue(len(response['data']) != 0)


    # #user_id not given in url, so error
    # def fails_invalid(self):
    #     response = self.client.get(reverse('category'))
    #     self.assertEquals(response.status_code, 404)

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down


# class GetTestOrder(TestCase):
#     #setUp method is called before each test in this class
#     #fixture = # JSON File 
#     def setUp(self):
#         #pass #nothing to set up
#         self.client = Client()

#     def test_success_response(self):
#         #assumes user with id 1 is stored in db
#         response = self.client.get(reverse('categories')).json()

#         #checks that response contains parameter order list & implicitly
#         # checks that the HTTP status code is 200
#         self.assertEquals(response['response'], 'success')
#         self.assertTrue(isinstance(response['data'], list))
#         self.assertTrue(len(response['data']) != 0)

#     # #user_id not given in url, so error
#     # def fails_invalid(self):
#     #     response = self.client.get(reverse('category'))
#     #     self.assertEquals(response.status_code, 404)

#     #tearDown method is called after each test
#     def tearDown(self):
#         pass #nothing to tear down

