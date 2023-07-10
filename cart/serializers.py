from rest_framework import serializers

from cart.models import CartItem
from store.serializers import ProductDetailSerializer


class AddItemToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('product', 'amount')




