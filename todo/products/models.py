from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    category = models.CharField(max_length=3000)
    image = models.CharField(max_length=3000000)
    discount_percentage = models.IntegerField()
    price = models.IntegerField()
    weight = models.IntegerField(default=0)