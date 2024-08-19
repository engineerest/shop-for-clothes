from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from decimal import Decimal

from Landing.core.models import *

PRODUCT_URL = reverse('shop:product-list')

def detail_url(product_id):
    return reverse('shop:product-detail', args=[product_id])
def create_product(user, **params):
    defaults = {
        'title': 'Name Product',
        'price': Decimal('25.00'),
        'description': 'Description Product',
        'image': 'image.png',
    }

    defaults.update(params)

    product = get_user_model().objects.create(user=user, **defaults)
    return product
class PublicProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')

    def test_get_products(self):
        product = get_user_model().objects.create(user=self.user, title='Chair')
        ShopProduct.objects.get(user=self.user, product=product)

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.data[0]['title'], product.title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_required(self):
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateProductAPITests(TestCase):
    def setUp(self):
        client = APIClient()
        client.force_authenticate(self.user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_products(self):
        product = get_user_model().objects.create(user=self.user, title='Chair')
        ShopProduct.objects.get(user=self.user, product=product)

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.data[0]['title'], product.title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_products(self):
        self.user = get_user_model().objects.create_user(email='user_sample@example.com')
        get_user_model().objects.create(user=self.user, title='Chair')
        product = get_user_model().objects.create(title='Table')

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], product.title)
        self.assertEqual(res.data[0]['id'], product.id)

    def test_remove_product(self):
        payload = {
            'title': 'Chair',
            'description': 'Description Chair',
            'price': Decimal("22.00"),
            'image': 'image.png',
            }
        self.assertEqual(ShopProduct.objects.count(), 1)

        res = self.client.delete(PRODUCT_URL, payload)

        self.assertEqual(res.data, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShopProduct.objects.count(), 0)

    def test_partial_update_product(self):
        original_link = 'http://example.com/products/1'
        product = create_product(user=self.user, title='Bed', link=original_link)
        payload = {
            'title': 'Chair',
        }

        url = detail_url(product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['link'], product.link)
        self.assertEqual(res.data['user'], product.user)

    def test_full_update_product(self):
        product = create_product(user=self.user, title='Bed',
                                 link='http://example.com/products/1', description='Sample Description')
        payload = {
            'title': 'Bed',
            'description': 'Sample Description',
            'price': Decimal("25.00"),
            'image': 'image.png',
        }
        url = detail_url(product.id)
        res = self.client.put(url, payload)

        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)
        self.assertEqual(product.user, self.user)

    def test_buy_product(self, user, **params):
        default = {
            'title': 'Shirt',
            'description': 'Sample Shirt',
            'price': Decimal("25.00"),
            'image': 'shirt.png',
        }

        account = {
            'nickname': 'user1',
            'email': 'user@example.com',
            'bill': Decimal("50.00"),
        }

        account.update(params)
        default.update(params)
        product = create_product(user=self.user, **default)

        res_product = self.client.get(PRODUCT_URL, default)
        res_account = self.client.get(PRODUCT_URL, account)

        self.assertEqual(res_product.status_code, status.HTTP_201_CREATED)
        product.refresh_from_db()
        self.assertEqual(res_product.data[0]['title'], default['title'])
        self.assertIn(res_product.data['price'], res_account.data['bill'])
