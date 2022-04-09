from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User
from django.http import Http404

from cart.models import Cart, CartProductMapping
from products.models import Product
from products.serializers import ProductSerializer

class CartMappingSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProductMapping
        fields = ['quantity', 'product']

# Serializers define the API representation.
class CartSerializer(serializers.ModelSerializer):
    cart = CartMappingSerializer(many=True)
    total = serializers.IntegerField(required=False)

    class Meta:
        model = Cart
        fields = ['cart', 'total', 'id']


class CartCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def get_product(self, id):
      try:
        return Product.objects.get(id=id)
      except:
        raise Http404

    def create(self, validated_data):
      quantity = validated_data.get('quantity')
      product  = self.get_product(validated_data.get('product_id'))
      cart = Cart.objects.create(total=(product.price * quantity))
      CartProductMapping.objects.create(product=product, cart=cart, quantity=validated_data.get('quantity')) 
      return cart

    def update(self, cart, validated_data):
      quantity = validated_data.get('quantity')
      product  = self.get_product(validated_data.get('product_id'))
      cart.total = cart.total + (product.price * quantity)
      cart.save()
      CartProductMapping.objects.create(product=product, cart=cart, quantity=validated_data.get('quantity')) 
      return cart