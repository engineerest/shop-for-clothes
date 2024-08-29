
from django.shortcuts import render
from django.views.generic import TemplateView
from .serializers import *
from Landing.core.models import *
from django.core.paginator import Paginator

class ProductsView(TemplateView):
    models = (ShopProduct, ShopCategory)
    template_name = 'shop/products.html'
    queryset = ShopProduct.objects.all()

    def index(self, request):
        return render(request, self.template_name)

    def get_queryset(self):
        return self.queryset

    def get_products(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return render(request, self.template_name, context=products)

    def get_products_dtos(self, request, serializer):
        serializer_product_dtos = ShopProductSerializer(ShopProduct.objects.all(), many=True)
        product_payload = {
            'product_name': serializer.data['name'],
            'product_description': serializer.data['description'],
            'product_short_description': serializer.data['short_description'],
            'product_price': serializer.data['price'],
            'product_price_with_discount': serializer.data['price_with_discount'],
            'product_discount': serializer.data['discount'],
            'product_quantity': serializer.data['quantity'],
            'product_image': serializer.data['image'],
            'product_category': serializer.data['category'],
        }
        serializer_product_dtos.save(product=product_payload)

        return render(request, self.template_name, context=product_payload)

    def page_counter(self, request, serializer):
        products = ShopProduct.objects.all()
        paginator = Paginator(products, products.count())
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        pages_serializer = ShopProductSerializer(page, many=True)

        return render(request, self.template_name, context=pages_serializer.data)


class ProductListView(TemplateView):
    models = (ShopProduct, ShopCategory)
    template_name = 'shop/products.html'
    queryset = ShopProduct.objects.all()

    def index(self, request):
        return render(request, 'shop/product-list.html')

    def get_queryset(self):
        return self.queryset

    def get_categories(self, request, serializer):
        serializer_categories = ShopCategorySerializer(ShopCategory.objects.filter(user=request.user), many=True)
        categories = ShopCategory.objects.get(pk=serializer.data['category'])
        serializer_categories.save(category=categories)

        return render(request, self.template_name, context=categories)

    def get_products(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return render(request, self.template_name, context=products)


class ProductDetailView(TemplateView):
    models = (ShopProduct, ShopCategory)
    template_name = 'shop/product-detail.html'
    queryset = ShopProduct.objects.all()

    def index(self, request):
        return render(request, self.template_name)

    def get_product_dtos(self, request, serializer):
        serializer_product_dtos = ShopProductSerializer(ShopProduct.objects.all(), many=True)
        product_payload = {
            'product_name': serializer.data['name'],
            'product_description': serializer.data['description'],
            'product_short_description': serializer.data['short_description'],
            'product_price': serializer.data['price'],
            'product_price_with_discount': serializer.data['price_with_discount'],
            'product_discount': serializer.data['discount'],
            'product_quantity': serializer.data['quantity'],
            'product_image': serializer.data['image'],
            'product_category': serializer.data['category'],
        }
        serializer_product_dtos.save(product=product_payload)

        return render(request, self.template_name, context=product_payload)

class CartView(TemplateView):
    models = (ShopProduct, ShopCategory, Cart)
    template_name = "shop/cart.html"
    def get_queryset(self, request):
        return Cart.objects.filter(product=request.user)

    def get_products(self, request, serializer):
        serializer_products = ShopProductSerializer(ShopProduct.objects.filter(user=request.user), many=True)
        products = ShopProduct.objects.get(pk=serializer.data['id'])
        serializer_products.save(product=products)

        return render(request, self.template_name, context={"cart_products": products})

    def get_cart_dtos(self, request, serializer):
        serializer_cart_dtos = Cart(Cart.objects.filter(product=request.user))
        cart_payload = {
            'cart_name': serializer.data['name'],
            'cart_quantity': serializer.data['quantity'],
            'cart_price': serializer.data['price'],
            'cart_image': serializer.data['image'],
            'cart_category': serializer.data['category'],
        }
        serializer_cart_dtos.save(cart_payload)

        return render(request, self.template_name, context=cart_payload)

    def get_total_price(self, request, serializer):
        serializer_cart = Cart.objects.filter(total_price=serializer.data['total_price'])
        total_price = {'total_price': serializer.data['total_price']}
        serializer_cart.update(total_price)

        return render(request, self.template_name, context=total_price)


    def change_product_quantity_greater(self, request, serializer):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.get(user=serializer.data['user'], product=serializer_product).quantity += 1
        serializer_product.update(quantity=serializer.data['quantity'])

        return render(request, self.template_name, context=serializer.data)

    def change_product_quantity_lower(self, request, serializer):
        serializer_product = ShopProduct.objects.get(pk=serializer.data['id'])
        Cart.objects.get(user=serializer.data['user'], product=serializer_product).quantity -= 1
        serializer_product.update(quantity=serializer.data['quantity'])

        if serializer.data['quantity'] == 0:
            return serializer_product.delete(serializer.data['id'])

        return render(request, self.template_name, context=serializer.data)


class CheckoutView(TemplateView):
    models = (ShopProduct, ShopCategory, Cart , Seller)
    template_name = "shop/checkout.html"

    def get_queryset(self, request, serializer):
        return Cart.objects.filter(product=serializer.data['id'])

    def get_seller_info(self, request, serializer):
        serializer_seller = Seller.objects.get(pk=serializer.data['id'])
        seller_payload = {
            'seller_name': serializer.data['name'],
            'seller_address': serializer.data['address'],
            'seller_phone': serializer.data['phone'],
            'seller_email': serializer.data['email'],
        }
        serializer_seller.save(seller_payload)

        return render(request, self.template_name, context=seller_payload)

    def get_checkout(self, request, serializer):
        serializer_checkout = Checkout.objects.get(product=serializer.data['id'])

        return render(request, self.template_name, context={'checkout': serializer_checkout})

    def get_checkout_dtos(self, request, serializer):
        serializer_checkout = Checkout.objects.get(product=serializer.data['id'])

        # checkout = Checkout.objects

        checkout_product_payload = {
            # 'product_name' : checkout.get(name=serializer.data['name']),
            'products' : serializer_checkout,
            'product_name': serializer.data['name'],
            'product_description': serializer.data['description'],
            'product_price': serializer.data['price'],
            'product_price_with_discount': serializer.data['price_with_discount'],
        }
        serializer_checkout.save(checkout_product_payload)

        return render(request, self.template_name, context=checkout_product_payload)
