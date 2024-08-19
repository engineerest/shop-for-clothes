from rest_framework import serializers
from django.contrib.auth import get_user_model

from Landing.core.models import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        # model = ContactSerializer
        pass