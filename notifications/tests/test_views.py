from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, override_settings

from notifications.tests.fixtures import FixtureUsers
from store.models import Product


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

class TestEmailNotifications(FixtureUsers, APITestCase):

    def setUp(self) -> None:
        super().setUp()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_email_messaging(self):
        Product.objects.create(id=1, product_name='product-name', description='description', price='1000', amount=10,
                               send_email_created=True, vendor=self.vendor, category=self.category, brand=self.brand)

        email_msg = mail.outbox
        self.assertEqual(len(email_msg), 2)
        self.assertIn('testuser2', email_msg[0].body)
        self.assertIn('http://127.0.0.1:8000/api/v1/store/products/1/', email_msg[0].body)

        self.assertIn('testuser3', email_msg[1].body)
        self.assertIn('http://127.0.0.1:8000/api/v1/store/products/1/', email_msg[1].body)


    def test_email_messaging_when_send_email_created_is_false(self):
        Product.objects.create(id=1, product_name='product-name', description='description', price='1000', amount=10,
                               send_email_created=False, vendor=self.vendor, category=self.category, brand=self.brand)

        email_msg = mail.outbox
        self.assertEqual(len(email_msg), 0)

