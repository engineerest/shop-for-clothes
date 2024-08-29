from django.core.paginator import Paginator
from .serializers import serializers
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Landing.shop.serializers import *


class ProductsViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ShopProduct.objects.all()

    def get_queryset(self):
        return ShopProduct.objects.all()

    def perform_create(self, serializers):
        serializers.save(user=self.request.user)

    def get_products(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=self.request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return Response(serializer_products.data, status=status.HTTP_201_CREATED)


class ProductDetailViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_products_dtos(self, request, serializer):
        serializer_product_dtos = ShopProductSerializer(ShopProduct.objects.all(), many=True)
        product_payload = {
            'product_name' : serializer.data['name'],
            'product_description' : serializer.data['description'],
            'product_short_description' : serializer.data['short_description'],
            'product_price' : serializer.data['price'],
            'product_price_with_discount' : serializer.data['price_with_discount'],
            'product_discount' : serializer.data['discount'],
            'product_quantity' : serializer.data['quantity'],
            'product_image' : serializer.data['image'],
            'product_category' : serializer.data['category'],
        }
        serializer_product_dtos.save(product=product_payload)

        return Response(serializer_product_dtos.data)

class ProductListViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartViewSet(viewsets.ViewSet, APIView):
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def add_to_cart(self, serializer):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.create(user=serializer.data['user'], product=serializer_product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove_from_cart(self, serializer):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.filter(user=serializer.data['user'], product=serializer_product).delete()

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def get_cart_products(self, serializer, request):
        serializer_cart = Cart.objects.get(pk=serializer.data['id'])
        serializer_cart_product_dtos = ShopProductSerializer(ShopProduct.objects.all(), many=True)
        serializer_cart_products = ShopProductSerializer(serializer_cart, many=True)

        cart_payload = {
            'cart_name': serializer.data['name'],
            'cart_description': serializer.data['description'],
            'cart_price': serializer.data['price'],
            'cart_price_with_discount': serializer.data['price_with_discount'],
            'cart_discount': serializer.data['discount'],
            'cart_quantity': serializer.data['quantity'],
            'cart_image': serializer.data['image'],
        }
        serializer_cart_product_dtos.save(cart=cart_payload)

        return Response(data=(serializer_cart_product_dtos.data, serializer_cart_products.data), status=status.HTTP_200_OK)


    def get_total_price(self, serializer, request):
        cart = Cart.objects.get(user=serializer.data['user'], product=serializer.data['product'])
        total_price = cart.price * cart.quantity

        return Response(serializer.data, status=status.HTTP_200_OK)