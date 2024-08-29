from rest_framework import serializers
from django.contrib.auth import get_user_model

from Landing.core.models import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone', 'address', 'city', 'country']

        read_only_fields = ['id', 'first_name', 'last_name', 'email',
                            'phone', 'city', 'country']

    def get_user(self, obj):
        return get_user_model().objects.get(pk=obj.id)

    def get(self):
        user = self.context['request'].user
        serializer = ContactSerializer(user)
        return serializer.data



