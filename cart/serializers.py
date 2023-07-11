from django.db.models import Subquery, Sum, F
from rest_framework import serializers

from cart.models import CartItem, Cart
from store.models import Product
from store.serializers import ProductListSerializer


class AddItemToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('product', 'amount')


class CartSummarySerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()
    product_amount = serializers.SerializerMethodField()
    total_regular_price = serializers.SerializerMethodField()
    total_price_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('product_amount', 'total_regular_price', 'total_price_with_discount', 'products')

    def get_products(self, instance):
        products_queryset = Product.objects.filter(
            pk__in=Subquery(
                instance.items.all().values('product')
            )
        )
        serializer = ProductListSerializer(products_queryset, many=True, context=self.context)
        return serializer.data

    def get_product_amount(self, instance):
        products = instance.items.all()
        amount = products.aggregate(Sum('amount')).get('amount__sum')
        return amount or 0

    def get_total_regular_price(self, instance):
        regular_price = instance.items.aggregate(
            total_regular_price=Sum('product__price')
        ).get('total_regular_price')
        return regular_price or 0

    def get_total_price_with_discount(self, instance):
        price_with_discount = instance.items.aggregate(
            total_price_with_discount=Sum(
                F('product__price') - (F('product__price') / 100 * F('product__discount_percent')),
            )
        ).get('total_price_with_discount')
        return price_with_discount or 0


class DeleteItemFromCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('product',)


