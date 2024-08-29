from django.urls import path, include

from .views import *
from .viewsets import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('contact', ContactViewSet, basename='contact')

urlpatterns = [
    # path('', include(router.urls)),
    path('contact/', ContactView.as_view(), name='contact'),
    # path('about/', AboutView.as_view(), name='about'),
    path('', IndexView.as_view(), name='home'),
]