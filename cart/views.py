import uuid

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import (AddItemToCart, CartSummarySerializer,
                              DeleteItemFromCartSerializer, UpdateCartItem)
from store.models import Product


class CartAddAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AddItemToCart(data=request.data)
        if serializer.is_valid():
            user_session = request.session.get('user_session')
            session_id = user_session or str(uuid.uuid4())

            if not user_session:
                request.session['user_session'] = session_id

            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(owner=request.user, session_id=session_id)
            else:
                cart, created = Cart.objects.get_or_create(session_id=session_id)

            product_id = serializer.data.get('product_id')
            amount = serializer.data.get('amount')

            try:
                Product.objects.get(id=product_id)
            except Product.DoesNotExist as err:
                return Response(data={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = CartItem.objects.get(product_id=product_id, cart=cart)
                product.amount += amount
                product.save()
            except CartItem.DoesNotExist:
                CartItem.objects.create(cart=cart, product_id=product_id, amount=amount)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartSummaryAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSummarySerializer


class DeleteCartItemAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        serializer = DeleteItemFromCartSerializer(data=request.data)
        if serializer.is_valid():
            cart_item_id = serializer.data.get('cart_item_id')
            user_session = request.session.get('user_session')

            try:
                CartItem.objects.get(id=cart_item_id)
            except CartItem.DoesNotExist as err:
                return Response(data={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

            if request.user.is_authenticated:
                cart = Cart.objects.get(session_id=user_session, owner=request.user)
            else:
                cart = Cart.objects.get(session_id=user_session)

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

            if request.user.is_authenticated:
                cart = Cart.objects.get(owner=request.user, session_id=session_id)
            else:
                cart = Cart.objects.get(session_id=session_id)

            item_to_update = CartItem.objects.get(cart=cart, id=cart_item_id)
            item_to_update.amount = amount
            item_to_update.save()
            return Response(data={"message": "successfully updated"}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)





