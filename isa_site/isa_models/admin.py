from django.contrib import admin
from .models import User, Product, ProductSnapshot, Order, Category, Condition

admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductSnapshot)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Condition)