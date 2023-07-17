import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartItem
from cart.serializers import AddItemToCart, UpdateCartItem
from store.tests.fixtures import FixtureTestCartData, FixtureTestData


class TestAddProductToCart(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = 'add-to-cart'

    def test_add_product_to_cart_user_is_not_authenticated(self):
        response = self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                             'amount': AddItemToCart.ONE})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.all().first()
        cart_items = CartItem.objects.all().first()

        self.assertEqual(cart.owner, None)
        self.assertEqual(cart_items.product, self.product1)

    def test_add_product_to_cart_user_is_authenticated(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                             'amount': AddItemToCart.ONE})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.all().first()
        cart_items = CartItem.objects.all().first()

        self.assertEqual(cart.owner, self.user1)
        self.assertEqual(cart_items.product, self.product1)

    def test_add_product_to_cart_not_specifying_product(self):
        response = self.client.post(reverse(self.url), data={'amount': AddItemToCart.ONE})
        cart_items = CartItem.objects.all()
        self.assertEqual(len(cart_items), 0)

    def test_add_product_to_cart_not_specifying_amount(self):
        self.client.post(reverse(self.url), data={'product_id': self.product1.id})
        cart_items = CartItem.objects.all()
        self.assertEqual(len(cart_items), 0)

    def test_add_product_that_does_not_exist(self):
        response = self.client.post(reverse(self.url), data={'product_id': 30})

    def test_get_session_key_user_is_not_authenticated(self):
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.ONE})

        client_session = self.client.session['user_session']

        session_id = Cart.objects.get(session_id=client_session)
        self.assertIsNotNone(session_id)

    def test_get_session_key_user_is_authenticated(self):
        self.client.force_authenticate(self.user1)
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.ONE})

        client_session = self.client.session['user_session']
        session_id = Cart.objects.get(session_id=client_session)

        self.assertIsNotNone(session_id)

    def test_add_second_product_to_cart(self):
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.ONE})
        self.client.post(reverse(self.url), data={'product_id': self.product2.id,
                                                  'amount': AddItemToCart.THREE})

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
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.ONE})
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.ONE})
        self.client.post(reverse(self.url), data={'product_id': self.product1.id,
                                                  'amount': AddItemToCart.THREE})

        self.client.post(reverse(self.url), data={'product_id': self.product2.id,
                                                  'amount': AddItemToCart.ONE})

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
        self.client.post(reverse(self.url), data={'product_id': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product_id': self.product1.id, 'amount': 1})
        self.client.post(reverse(self.url), data={'product_id': self.product2.id, 'amount': 3})
        self.client.post(reverse(self.url), data={'product_id': self.product3.id, 'amount': 1})

        cart = Cart.objects.get(session_id=self.client.session['user_session'])
        cart_items = CartItem.objects.filter(cart=cart)
        product1_item = CartItem.objects.get(product=self.product1)
        product2_item = CartItem.objects.get(product=self.product2)

        self.assertEqual(cart.owner, self.user1)
        self.assertEqual(len(Cart.objects.all()), 1)
        self.assertEqual(len(cart_items), 3)
        self.assertEqual(product1_item.amount, 2)
        self.assertEqual(product2_item.amount, 3)


class TestCartSummary(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('cart-summary')

    def test_get_card_response_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cart_response_authenticated(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteItemFromCart(FixtureTestCartData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = reverse('cart-item-delete')

        # Obtaining session key for product cart
        self.client.post(reverse('add-to-cart'), data={'product_id': self.product1.id,
                                                       'amount': AddItemToCart.ONE})
        session_key = self.client.session['user_session']
        self.cart = Cart.objects.get(session_id=session_key)
        self.cart_item = CartItem.objects.get(cart=self.cart, product=self.product1)


    def test_delete_request(self):

        response = self.client.delete(self.url, data={'cart_item_id': self.cart_item.id})

        cart_objects = self.cart.items.all()
        self.assertEqual(len(cart_objects), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_does_not_exist(self):
        response = self.client.delete(self.url, data={'cart_item_id': 30})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_item_that_is_owned_by_another_user(self):
        self.client.force_authenticate(self.user1)
        try:
            response = self.client.delete(self.url, data={'cart_item_id': self.cart_item.id,
                                                          'amount': UpdateCartItem.THREE})
        except Cart.DoesNotExist:
            assert True
        else:
            assert False


class TestCartUpdate(FixtureTestCartData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = reverse('cart-update')

        # Obtaining session key for product cart
        self.client.post(reverse('add-to-cart'), data={'product_id': self.product1.id,
                                                       'amount': UpdateCartItem.ONE})
        session_key = self.client.session['user_session']
        self.cart = Cart.objects.get(session_id=session_key)
        self.cart_item = CartItem.objects.get(cart=self.cart, product=self.product1)

    def test_update_cart_item_response(self):
        response = self.client.put(self.url, data={'cart_item_id': self.cart_item.id,
                                   'amount': UpdateCartItem.THREE})
        self.cart_item.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cart_item.amount, 3)

    def test_update_item_that_is_owned_by_another_user(self):
        self.client.force_authenticate(self.user1)
        try:
            response = self.client.put(self.url, data={'cart_item_id': self.cart_item.id,
                                                       'amount': UpdateCartItem.THREE})
        except Cart.DoesNotExist:
            assert True
        else:
            assert False

    def test_update_item_that_does_not_exist(self):
        response = self.client.put(self.url, data={'cart_item_id': 50,
                                                   'amount': UpdateCartItem.THREE})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



