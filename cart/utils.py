from django.core.exceptions import BadRequest
from rest_framework.request import Request

from cart.models import Cart, CartItem
from store.models import Product


class AddItemToCartHelper:

    def __init__(self, request: Request, session_id: str, product_id: int) -> None:
        self.request = request
        self.session_id = session_id
        self.product_id = product_id

    def get_or_create_cart(self) -> Cart:
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(owner=self.request.user, session_id=self.session_id)
        else:
            cart, created = Cart.objects.get_or_create(session_id=self.session_id)

        return cart

    def get_or_create_cart_item(self, amount: int, cart: Cart) -> None:
        try:
            product = CartItem.objects.get(product_id=self.product_id, cart=cart)
            product.amount += amount
            product.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product_id=self.product_id, amount=amount)

    def get_product_or_400_err(self):
        try:
            Product.objects.get(id=self.product_id)
        except Product.DoesNotExist as err:
            raise BadRequest(str(err))


class GetCartHelperMixin:

    def __init__(self, request: Request, session_id: str, cart_item_id: int) -> None:
        self.request = request
        self.session_id = session_id
        self.cart_item_id = cart_item_id

    def get_cart(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(session_id=self.session_id, owner=self.request.user)
        else:
            cart = Cart.objects.get(session_id=self.session_id)

        return cart


class DeleteItemFromCartHelper(GetCartHelperMixin):

    def get_cart_item_or_400_err(self):
        try:
            CartItem.objects.get(id=self.cart_item_id)
        except CartItem.DoesNotExist as err:
            raise BadRequest(str(err))


class UpdateItemFromCartHelper(GetCartHelperMixin):

    def update_cart_item_or_404(self, cart: Cart):
        try:
            item_to_update = CartItem.objects.get(cart=cart, id=self.cart_item_id)
        except CartItem.DoesNotExist as err:
            raise BadRequest(str(err))
        return item_to_update
