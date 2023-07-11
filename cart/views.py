import uuid

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import AddItemToCartSerializer, CartSummarySerializer, DeleteItemFromCartSerializer


class CartAddAPIView(CreateAPIView):

    serializer_class = AddItemToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddItemToCartSerializer(data=request.data)
        if serializer.is_valid():
            user_session = request.session.get('user_session')
            session_id = user_session or str(uuid.uuid4())

            if request.user.is_authenticated:
                obj, created = Cart.objects.get_or_create(owner=request.user, session_id=session_id)
            else:
                obj, created = Cart.objects.get_or_create(session_id=session_id)

            if not user_session:
                request.session['user_session'] = session_id

            product_id = serializer.data.get('product')
            amount = serializer.data.get('amount')

            try:
                product = CartItem.objects.get(product_id=product_id, cart=obj)
                product.amount += amount
                product.save()
            except CartItem.DoesNotExist:
                CartItem.objects.create(cart=obj, product_id=product_id, amount=amount)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartSummaryAPIView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSummarySerializer


class DeleteCartItemAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        serializer = DeleteItemFromCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.data.get('product')
            user_session = request.session.get('user_session')

            if request.user.is_authenticated:
                cart = Cart.objects.get(session_id=user_session, owner=request.user)
            else:
                cart = Cart.objects.get(session_id=user_session)

            item_to_del = CartItem.objects.get(cart=cart, product_id=product_id)
            item_to_del.delete()
            return Response(data={"message": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_200_OK)
