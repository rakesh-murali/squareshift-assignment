from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import functools
import json

from cart.serializers import CartSerializer, CartCreateSerializer
from cart.models import Cart, CartProductMapping
from products.models import Product
from cart.constants import SHIPPING_COST, DISTANCE, WEIGHT

class CartList(APIView):

  def get_product(self, id):
    try:
      product = Product.objects.get(id=id)
      return product
    except:
      raise Http404

  def post (self, request):
    serializer = CartCreateSerializer(data=request.data)
    if (serializer.is_valid()):
      serializer.save()
      return Response({ "cart": "Added Successfully" }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request):
    carts = Cart.objects.all()
    cart_data = CartSerializer(carts, many=True)
    return Response(cart_data.data, status=status.HTTP_200_OK)

class CartDetail(APIView):

  def get_cart(self, id):
    try:
      product = Cart.objects.get(id=id)
      return product
    except:
      raise Http404

  def post (self, request, pk):
    product_id = request.data.get('product_id')
    cart = self.get_cart(pk)
    serializer = CartCreateSerializer(cart, data=request.data)
    if (serializer.is_valid()):
      serializer.save()
      return Response({ "cart": "Added Successfully" }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request, pk):
    cart = self.get_cart(pk)
    cart_data = CartSerializer(cart)
    return Response(cart_data.data, status=status.HTTP_200_OK)

  def delete (self, request, pk):
    try:
      cart = Cart.objects.get(id=pk)
    except:
      return status.HTTP_404_NOT_FOUND
    cart.delete()
    return HttpResponse(status=status.HTTP_200_OK)

class CartShipping(APIView):

  def get_shipping_table_index (self, input_list, value):
      for i in range(len(input_list) - 1):
        if (input_list[i] <= value and input_list[i+1] >= value):
          return i
      return 0

  
  def get (self, request, pk, pn):
    x = requests.get('https://e-commerce-api-recruitment.herokuapp.com/warehouse/distance?postal_code='+ str(pn))
    if(x.status_code == 200):
      cart = self.get_cart(pk)
      response = json.loads(x.content)
      km = response['distance_in_kilometers']
      WEIGHT_INDEX, DISTANCE_INDEX = None, None

      DISTANCE_INDEX = self.get_shipping_table_index(DISTANCE, km)
      total_weight, discount_cost = self.get_discount_terms(pk)
      WEIGHT_INDEX = self.get_shipping_table_index(WEIGHT, total_weight)
      shipping_cost = SHIPPING_COST[WEIGHT_INDEX][DISTANCE_INDEX]
      total = (cart.total + shipping_cost) - discount_cost
      return Response({ "total_cart_value": total }, status=status.HTTP_200_OK)
    else:
      return Response({error: 'Invalid Pincode'}, status=status.HTTP_400_BAD_REQUEST)


  def get_cart(self, id):
    try:
      product = Cart.objects.get(id=id)
      return product
    except:
      raise Http404

  def get_discount_terms (self, pk):
    total_weight, discount_cost = 0, 0
    cart_mapping = CartProductMapping.objects.filter(cart_id=pk)
    for a in cart_mapping:
      total_weight += a.product.weight
      discount_cost += a.product.price * (a.product.discount_percentage/100)
    return total_weight, discount_cost

  


