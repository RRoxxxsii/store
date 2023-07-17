from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, override_settings

from account.models import Customer
from notifications.tests.fixtures import FixtureUsers
from store.models import Brand, Category, Product, Vendor


class TestSubscribeOnMailListing(FixtureUsers, APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('mail_listing_subscribe')

    def test_subscribe_on_mail_listing_authenticated(self):
        self.client.force_authenticate(self.user1)
        response = self.client.put(self.url)
        self.user1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.on_mail_listing, True)

    def test_unsubscribe_on_mail_listing_authenticated(self):
        self.client.force_authenticate(self.user2)
        response = self.client.put(self.url)
        self.user1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.on_mail_listing, False)


    def test_subscribe_on_mail_listing_not_authenticated(self):
        response = self.client.put(self.url)
        self.user1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.user1.on_mail_listing, False)


class TestEmailNotifications(APITestCase):

    def setUp(self) -> None:

        self.user1 = Customer.objects.create(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                             mobile='88005553535')

        self.user2 = Customer.objects.create(user_name='testuser2', email='testuser2@gmail.com',
                                             password='somepswrd1', mobile='88005553536', on_mail_listing=True)

        self.user3 = Customer.objects.create(user_name='testuser3', email='testuser3@gmail.com',
                                             password='somepswrd1', mobile='88005553537', on_mail_listing=True)

        self.vendor = Vendor.objects.create(vendor_name='vendor', description='description')

        self.category = Category.objects.create(category_name='category', description='description', slug='category',
                                                is_parent_category=True)

        self.brand = Brand.objects.create(brand_name='brand')

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_email_messaging(self):
        Product.objects.create(id=1, product_name='product-name', description='description', price='1000', amount=10,
                               send_email_created=True, vendor=self.vendor, category=self.category, brand=self.brand)

        email_msg = mail.outbox
        self.assertEqual(len(email_msg), 2)
        self.assertIn('testuser2', email_msg[0].body)
        self.assertIn('http://127.0.0.1:8000/api/v1/store/products/1/', email_msg[0].body)

        self.assertIn('testuser3', email_msg[1].body)
        self.assertIn('http://127.0.0.1:8000/api/v1/store/products/1/', email_msg[1].body)


    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_email_messaging_when_send_email_created_is_false(self):
        Product.objects.create(id=1, product_name='product-name', description='description', price='1000', amount=10,
                               send_email_created=False, vendor=self.vendor, category=self.category, brand=self.brand)

        email_msg = mail.outbox
        self.assertEqual(len(email_msg), 0)

