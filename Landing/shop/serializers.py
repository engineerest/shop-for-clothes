
from rest_framework import serializers

from Landing.core.models import *

class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['id','name','price','image','description', 'category']
        read_only_fields = ['id','name','price','image','description', 'category']

    def get(self, validated_data):
        products = ShopProduct.objects.all()
        serializer = ShopProductSerializer(products, many=True)

        return serializer.data

    def create(self, validated_data):
        return ShopProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.pop('name', instance.name)
        instance.price = validated_data.pop('price', instance.price)
        instance.image = validated_data.pop('image', instance.image)
        instance.description = validated_data.pop('description', instance.description)

        return instance
class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = ['id','name', 'image']
        read_only_fields = ['id']

    def get(self, validated_data):
        categories = ShopCategory.objects.all()
        serializer = ShopCategorySerializer(categories, many=True)

        return serializer.data

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id']

    def get(self, validated_data):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)

        return serializer.data

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        cart = Cart.objects.get(id=instance.id)
        cart.name = validated_data.pop('name', cart.name)
        cart.image = validated_data.pop('image', cart.image)
        cart.description = validated_data.pop('description', cart.description)
        cart.save()

        return cart

    def delete(self, instance):
        cart = Cart.objects.get(id=instance.id)
        cart.delete()

        return cart

    def remove(self, instance):
        cart = Cart.objects.get(id=instance.id)
        cart.delete()

        return cart




