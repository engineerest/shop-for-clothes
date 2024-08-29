from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Landing.shop.views import *

from .viewsets import *

router = DefaultRouter()

router.register('shop', ProductsViewSet, basename='shop')
router.register('product-list', ProductListViewSet, basename='product-list')
router.register('product-detail', ProductDetailViewSet, basename='product-detail')
router.register('cart', CartViewSet, basename='cart')
# router.register('checkout', CheckoutViewSet, basename='checkout')

urlpatterns = [
    # path('', include(router.urls)),
    path('', ProductsView.as_view(), name='products'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('detail-product/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='product_checkout'),
]