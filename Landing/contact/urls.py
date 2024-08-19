from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from Landing.contact import views

router = DefaultRouter()
# router.register('contact', views.ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]