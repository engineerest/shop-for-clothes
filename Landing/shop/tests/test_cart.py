from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from Landing.core.models import *

CART_URL = reverse('cart:cart_list')

class PublicCartApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')

    def test_login_required(self):
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateCartApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_cart(self):
        cart = Cart.objects.all()

        res = self.client.get(CART_URL, cart)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        cart = Cart.objects.all()
        product = get_user_model().objects.create(user=self.user, name='pants')
        cart.save(product)

        res = self.client.post(CART_URL, [cart, product])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(product, cart)
        self.assertEqual(Cart.objects.count(), 1)

    def test_remove_from_cart(self):
        cart = Cart.objects.all()
        product = get_user_model().objects.create(user=self.user, name='pants')
        cart.save(product)

        res = self.client.delete(CART_URL, [cart, product])

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(product, cart)
        self.assertEqual(Cart.objects.count(), 0)

    def test_change_greater_product_quantity(self):
        cart = Cart.objects.all()
        product = get_user_model().objects.create(user=self.user, name='pants', quantity=1)
        product_quantity = product.quantity
        cart.save(product)

        product = get_user_model().objects.create(user=self.user, name='pants', quantity=product_quantity + 1)

        res = self.client.post(CART_URL, [cart, product])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(product, cart)
        self.assertNotIn(product_quantity, product)

    def test_change_lesser_product_quantity(self):
        cart = Cart.objects.all()
        product = get_user_model().objects.create(user=self.user, name='pants', quantity=2)
        product_quantity = product.quantity
        cart.save(product)

        product = get_user_model().objects.create(user=self.user, name='pants', quantity=product_quantity - 1)

        res = self.client.post(CART_URL, [cart, product])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(product, cart)
        self.assertNotIn(product_quantity, product)


