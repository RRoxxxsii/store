from django.urls import reverse
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from store.tests.fixtures import FixtureTestData


class TestAddProductToCart(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = 'add-to-cart'

    def test_add_product_to_cart_user_is_not_authenticated(self):
        response = self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.assertEqual(response.status_code, 201)

        cart = Cart.objects.all().first()
        cart_items = CartItem.objects.all().first()

        self.assertEqual(cart.owner, None)
        self.assertEqual(cart_items.product, self.product1)

    def test_add_product_to_cart_user_is_authenticated(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.assertEqual(response.status_code, 201)

        cart = Cart.objects.all().first()
        cart_items = CartItem.objects.all().first()

        self.assertEqual(cart.owner, self.user1)
        self.assertEqual(cart_items.product, self.product1)

    def test_get_session_key_user_is_not_authenticated(self):
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        client_session = self.client.session['user_session']

        session_id = Cart.objects.get(session_id=client_session)
        self.assertIsNotNone(session_id)

    def test_get_session_key_user_is_authenticated(self):
        self.client.force_authenticate(self.user1)
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        client_session = self.client.session['user_session']
        session_id = Cart.objects.get(session_id=client_session)

        self.assertIsNotNone(session_id)

    def test_add_second_product_to_cart(self):
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product': self.product2.id, 'amount': 3})

        cart_items = CartItem.objects.all()
        self.assertEqual(len(cart_items), 2)

    def test_amount_of_products_in_queryset(self):
        """
        Test amount of products in queryset if one concrete product was added
        several times
        """
        pass

    def test_add_products_to_cart_if_already_exists_not_authenticated(self):
        """
        If a product is already in the cart and it's been added, the amount of product is
        supposed to be increased on the amount. So duplicates are not saved to CartItem model,
        is't amount just increases. User is not authenticated.
        """
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 3})

        self.client.post(reverse(self.url), data={'product': self.product2.id, 'amount': 1})

        cart = Cart.objects.get(session_id=self.client.session['user_session'])
        cart_items = CartItem.objects.filter(cart=cart)
        product1_item = CartItem.objects.get(product=self.product1)
        product2_item = CartItem.objects.get(product=self.product2)

        self.assertEqual(len(cart_items), 2)
        self.assertEqual(len(Cart.objects.all()), 1)
        self.assertEqual(product1_item.amount, 5)
        self.assertEqual(product2_item.amount, 1)


    def test_add_products_to_cart_if_already_exists_user_is_authenticated(self):
        """
        If a product is already in the cart and it's been added, the amount of product is
        supposed to be increased on the amount. So duplicates are not saved to CartItem model,
        is't amount just increases.
        """
        self.client.force_authenticate(self.user1)
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product': self.product2.id, 'amount': 3})
        self.client.post(reverse(self.url), data={'product': self.product3.id, 'amount': 1})

        cart = Cart.objects.get(session_id=self.client.session['user_session'])
        cart_items = CartItem.objects.filter(cart=cart)
        product1_item = CartItem.objects.get(product=self.product1)
        product2_item = CartItem.objects.get(product=self.product2)

        self.assertEqual(cart.owner, self.user1)
        self.assertEqual(len(Cart.objects.all()), 1)
        self.assertEqual(len(cart_items), 3)
        self.assertEqual(product1_item.amount, 2)
        self.assertEqual(product2_item.amount, 3)

