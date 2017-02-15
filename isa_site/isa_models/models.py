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

    def __str__(self):
        return "User: " + self.email

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "Category: " + self.name

class Condition(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "Condition: " + self.name

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    sold = models.BooleanField()
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)

    def __str__(self):
        return "Product: " + self.name

class ProductSnapshot(models.Model):
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.FloatField()
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)

    def __str__(self):
        return "Snapshot: " + self.name

class Order(models.Model):
    product_snapshot = models.ForeignKey(ProductSnapshot, on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_method = models.CharField(max_length=30)
    tracking_number = models.CharField(max_length=50)
    status = models.CharField(max_length=30)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='buyer')
    completed = models.BooleanField()
    buyer_rating = models.IntegerField(default=5)
    seller_rating = models.IntegerField(default=5)

    def __str__(self):
        return "Order: " + self.product_snapshot.name
