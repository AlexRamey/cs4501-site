from django.db import models

# Create your models here.
class User(models.Model):
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=16)
	ship_address = models.CharField(max_length=100)
	ship_city = models.CharField(max_length=100)
	ship_postal_code = models.CharField(max_length=16)
	ship_country = models.CharField(max_length=100)
	buyer_rating = models.FloatField(default=100.0)
	seller_rating = models.FloatField(default=100.0)

class Product(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=80)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.FloatField()
    stock = models.int()
    sold = models.BooleanField()
    condition_id = models.ForeignKey(Condition, on_delete=models.PROTECT)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_method = models.CharField(max_length=30)
    tracking_number = models.int()
    status = models.CharField(max_length=30)
    seller_id = models.ForeignKey(User, on_delete=models.PROTECT)
    buyer_id = models.ForeignKey(User, on_delete=models.PROTECT)
    completed = models.BooleanField()
    buyer_rating = models.int()
    seller_rating = models.int()

class Category(models.Model):
    name = models.CharField(max_length=30)

class Condition(models.Model):
    name = models.CharField(max_length=30)
