from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Landing.shop import views

router = DefaultRouter()

router.register('shop', views.ShopViewSet, basename='shop')
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]