from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User

from products.models import Product

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount_percentage', 'category', 'id']