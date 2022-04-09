from django.db import models
from datetime import datetime    

from products.models import Product

class Cart(models.Model):
    total = models.IntegerField()

class CartProductMapping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    quantity = models.IntegerField()