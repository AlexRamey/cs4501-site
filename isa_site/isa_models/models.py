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