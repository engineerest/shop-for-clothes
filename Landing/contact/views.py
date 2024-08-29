from django.shortcuts import render
from django.views.generic import TemplateView

from Landing.core.models import *
from Landing.contact.serializers import *

from Landing.shop.serializers import *
class ContactView(TemplateView):
    models = (Account, Seller)
    template_name = 'dashboard/contact.html'
    queryset = Seller.objects.all()

    def get_queryset(self):
        return self.queryset

    def index(self, request):
        return render(request, self.template_name)

    def get_seller_info(self, request, serializer):
        serializer_seller = ContactSerializer(Seller.objects.get(user=serializer.data['id']), many=True)
        seller_payload = {
            'seller': serializer.data,
            'email' : serializer.data['email'],
            'phone' : serializer.data['phone'],
            'address' : serializer.data['address'],
            'city' : serializer.data['city'],
            'country' : serializer.data['country'],
        }
        serializer_seller.save(user=seller_payload)

        return render(request, self.template_name, context=seller_payload)


class IndexView(TemplateView):
    models = (ShopProduct, ShopCategory)
    template_name = "dashboard/index.html"
    queryset = ShopProduct.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_products(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return render(request, self.template_name, {'products': products})

    def get_products_dtos(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=request.user), many=True)
        product_payload = {
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'price': serializer.data['price'],
            'discount': serializer.data['discount'],
            'price_with_discount': serializer.data['price_without_discount'],
            'image': serializer.data['image'],
            'description': serializer.data['description'],
            'short_description': serializer.data['short_description'],
            'category': serializer.data['category'],
        }
        serializer_products.save(product=product_payload)

        return render(request, self.template_name, context=product_payload)
