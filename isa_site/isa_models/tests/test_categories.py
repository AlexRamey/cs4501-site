from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from isa_models.models import Category

class GetTestCategoryList(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass #nothing to set up

    def success_response(self):
        #assumes user with id 1 is stored in db
        response = self.client.get('/categories')

        #checks that response contains parameter order list & implicitly
        # checks that the HTTP status code is 200
        self.assertContains(response, 'order_list')

    #user_id not given in url, so error
    def fails_invalid(self):
        response = self.client.get(reverse('category'))
        self.assertEquals(response.status_code, 404)

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down