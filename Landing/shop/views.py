
from django.core.paginator import Paginator
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from Landing.shop.serializers import *


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    product_queryset = ShopProduct.objects.all()

    def setUp(self, request):
        self.product_list = lambda product_list: render(request, 'shop/product-list.html', context=product_list)
        self.products = lambda products_payload: render(request, 'shop/products.html', context=products_payload)
        self.product_detail = lambda product_detail_payload: render(request, 'shop/product-detail.html', context=product_detail_payload)
        self.cart = lambda cart_payload: render(request, 'shop/cart.html', context=cart_payload)
        self.checkout = lambda checkout_payload: render(request, 'shop/checkout.html', context=checkout_payload)

    def get_queryset(self):
        return ShopProduct.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_categories(self, request, serializer):
        serializer_categories = ShopCategorySerializer(ShopCategory.objects.filter(user=self.request.user), many=True)
        categories = ShopCategory.objects.get(pk=serializer.data['category'])
        serializer_categories.save(category=categories)

        return (Response(serializer_categories.data),)

    def get_products(self, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=self.request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return (Response(serializer_products.data),)


    def get_products_dtos(self, serializer):
        serializer_products_dtos = ShopProductSerializer(ShopProduct.objects.all(), many=True)
        self.product_payload = {
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
        serializer_products_dtos.save(product=self.product_payload)

        return (Response(serializer_products_dtos.data),
                self.cart(serializer_products_dtos.data),
                self.checkout(serializer_products_dtos.data),
                self.products(serializer_products_dtos.data),
                self.product_detail(serializer_products_dtos.data),
                self.product_list(serializer_products_dtos.data)
                )



    def page_counter(self, request, serializer):
        products = ShopProduct.objects.all()

        paginator = Paginator(products, products.count())

        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        pages_serializer = ShopProductSerializer(page, many=True)

        return (Response(pages_serializer.data, status=status.HTTP_200_OK),
                self.cart(pages_serializer.data),
                self.checkout(pages_serializer.data),
                self.products(pages_serializer.data),
                self.product_detail(pages_serializer.data),
                self.product_list(pages_serializer.data))

class CartViewSet(viewsets.ViewSet):
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    product_queryset = Cart.objects.all()

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

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

        return (Response(data=(serializer_cart_product_dtos.data, serializer_cart_products.data), status=status.HTTP_200_OK),
                render(request, 'shop/cart.html', context=cart_payload),
                render(request, 'shop/cart.html', context={'cart': serializer_cart_products.data}))

    # def get_cart_products(self, serializer, request):
    #     serializer_cart = Cart.objects.get(pk=serializer.data['id'])
    #     serializer_cart_products = ShopProductSerializer(serializer_cart, many=True)
    #
    #     return (Response(serializer_cart_products.data),
    #             render(request, 'shop/cart.html', context={'cart': serializer_cart_products.data}),)


    def change_greater_product_quantity(self, serializer, request):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.get(user=serializer.data['user'], product=serializer_product).quantity += 1
        serializer_product.update(quantity=serializer.data['quantity'])

        return (Response(serializer.data, status=status.HTTP_200_OK),
                render(request, 'shop/cart.html', {'quantity': serializer.data['quantity']}))

    def change_lower_product_quantity(self, serializer, request):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.get(user=serializer.data['user'], product=serializer_product).quantity -= 1
        serializer_product.update(quantity=serializer.data['quantity'])
        if serializer.data['quantity'] == 0:
            serializer_product.delete(serializer.data['id'])

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return (Response(serializer.data, status=status.HTTP_200_OK),
                render(request, 'shop/cart.html', {'quantity': serializer.data['quantity']}))

    def get_total_price(self, serializer, request):
        cart = Cart.objects.get(user=serializer.data['user'], product=serializer.data['product'])
        total_price = cart.price * cart.quantity

        return (Response(serializer.data, status=status.HTTP_200_OK),
                render(request, 'shop/cart.html', context=total_price))