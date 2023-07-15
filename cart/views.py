import uuid

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import (AddItemToCart, CartSummarySerializer,
                              DeleteItemFromCartSerializer, UpdateCartItem)
from cart.utils import AddItemToCartHelper, DeleteItemFromCartHelper, UpdateItemFromCartHelper
from store.models import Product


class CartSummaryAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSummarySerializer


class CartAddAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AddItemToCart(data=request.data)
        if serializer.is_valid():
            user_session = request.session.get('user_session')
            session_id = user_session or str(uuid.uuid4())

            if not user_session:
                request.session['user_session'] = session_id

            product_id = serializer.data.get('product_id')
            amount = serializer.data.get('amount')

            cart_item_adder = AddItemToCartHelper(request=request, session_id=session_id, product_id=product_id)
            cart = cart_item_adder.get_or_create_cart()
            cart_item_adder.get_product_or_400_err()
            cart_item_adder.get_or_create_cart_item(amount=amount, cart=cart)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItemAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        serializer = DeleteItemFromCartSerializer(data=request.data)
        if serializer.is_valid():
            cart_item_id = serializer.data.get('cart_item_id')
            session_id = request.session.get('user_session')

            cart_item_deleter = DeleteItemFromCartHelper(request=request, session_id=session_id,
                                                         cart_item_id=cart_item_id)
            cart_item_deleter.get_cart_item_or_400_err()
            cart = cart_item_deleter.get_cart()
            item_to_del = CartItem.objects.get(cart=cart, id=cart_item_id)
            item_to_del.delete()

            return Response(data={"message": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)


class UpdateCartAPIView(APIView):

    def put(self, request, *args, **kwargs):
        serializer = UpdateCartItem(data=request.data)
        if serializer.is_valid():
            user_session = request.session.get('user_session')
            session_id = user_session or str(uuid.uuid4())

            cart_item_id = serializer.data.get('cart_item_id')
            amount = serializer.data.get('amount')

            cart_item_updater = UpdateItemFromCartHelper(request=request, session_id=session_id,
                                                         cart_item_id=cart_item_id)
            cart = cart_item_updater.get_cart()
            item_to_update = cart_item_updater.update_cart_item_or_404(cart)

            item_to_update.amount = amount
            item_to_update.save()
            return Response(data={"message": "successfully updated"}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)





