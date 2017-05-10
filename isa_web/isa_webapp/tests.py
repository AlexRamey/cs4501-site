from django.test import TestCase

# Create your tests here.
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AccountTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def tearDown(self):
        self.driver.close()

    def test_register(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8000/isa_web/createaccount")

        email = driver.find_element_by_id('id_email')
        password = driver.find_element_by_id('id_password')
        first_name = driver.find_element_by_id('id_first_name')
        last_name = driver.find_element_by_id('id_last_name')
        phone_number = driver.find_element_by_id('id_phone_number')
        ship_address = driver.find_element_by_id('id_ship_address')
        ship_city = driver.find_element_by_id('id_ship_city')
        ship_postal_code = driver.find_element_by_id('id_ship_postal_code')
        ship_country = driver.find_element_by_id('id_ship_country')
        submit = driver.find_element_by_id('submit_button')

        email.send_keys('adama1234@gmail.com')
        password.send_keys('123456')
        first_name.send_keys('Adam')
        last_name.send_keys('Guo')
        phone_number.send_keys('6104705820')
        ship_address.send_keys('1111 wsd')
        ship_city.send_keys('cville')
        ship_postal_code.send_keys('22903')
        ship_country.send_keys('usa')

        submit.click()

        assert 'Welcome' in driver.page_source

    def test_create_listing(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8000/isa_web/createlisting")

        name = driver.find_element_by_id('id_name')
        description = driver.find_element_by_id('id_description')
        category = driver.find_element_by_id('id_category')
        condition = driver.find_element_by_id('id_condition')
        price = driver.find_element_by_id('id_price')
        stock = driver.find_element_by_id('id_stock')
        submit = driver.find_element_by_id('submit_button')

        name.send_keys('New Shoes')
        description.send_keys('Air Jordan 11')
        category.SelectByValue('1')
        condition.SelectByValue('5')
        price.send_keys('100')
        stock.send_keys('1')

        submit.click()

        assert 'New Shoes' in driver.page_source

    def test_search(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8000/isa_web/search")

        search = driver.find_element_by_name('search_query')
        submit = driver.find_element_by_id('search_button')

        search.send_keys('new')

        submit.click()

        assert 'New Shoes' in driver.page_source


