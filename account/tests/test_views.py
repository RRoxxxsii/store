import re

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from account.models import Customer, CustomerProfile
from django.urls import reverse
from django.core import mail


class TestUserCreateAccountAPIView(APITestCase):

    def setUp(self) -> None:
        self.user = Customer.objects.create_user(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                                 mobile='88005553535')
        self.url = reverse('register')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_request_user_not_authenticated(self):
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser2')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user)

    def test_get_request_user_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_request_user_authenticated(self):
        """
        User is not supposed to be created
        """
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1ba#3!', 'password2': 'pWrDLoL1#3!'})
        try:
            Customer.objects.get(user_name='testuser2')
        except ObjectDoesNotExist:
            assert True
        else:
            assert False

    def test_different_passwords(self):
        """
        User is not supposed to be created
        """
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1ba#3!', 'password2': 'pWrDLoL1#3!'})

        try:
            Customer.objects.get(user_name='testuser2')
        except ObjectDoesNotExist:
            assert True
        else:
            assert False
        self.assertEqual(eval(response.content.decode()), {'password': ['Пароли не совпадают.']})

    def test_user_not_is_active_after_creation(self):
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser2')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user)


class TestConfirmationRegisterGetEmail(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('register')

    def test_get_email(self):
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        email_msg = mail.outbox

        self.assertEqual(len(email_msg), 1)

    def test_get_email_if_data_not_correct(self):
        """
        If data user post data is not correct getting email is not supposed
        """
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1ba#3!', 'password2': 'pWrDLoL1#3!'})

        email_msg = mail.outbox

        self.assertEqual(len(email_msg), 0)


class TestMakeAccountActivateByEmail(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('register')
        self.url_confirm_email = reverse('confirm_email_view')

    def test_activate_account(self):
        response = self.client.post(self.url, data={'user_name': 'testuser2', 'email': 'testuser2@gmail.com',
                                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser2')
        self.assertFalse(user.is_active)
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersonalProfile(APITestCase):

    def setUp(self) -> None:
        self.user = Customer.objects.create_user(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                                 mobile='88005553535')
        self.url = reverse('profile')

    def test_get_personal_profile_page_when_not_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_personal_profile_when_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_personal_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data={'city': 'Иркутск'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.customer_profile.city, 'Иркутск')



