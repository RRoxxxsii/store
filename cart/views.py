import uuid

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import AddItemToCartSerializer


session = {'user_session': 'some_key'}


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