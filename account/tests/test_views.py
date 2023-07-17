import re

from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Customer, CustomerProfile


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
        self.user = Customer.objects.create_user(user_name='testuser1', email='testuser1@gmail.com',
                                                 password='somepswrd1', mobile='88005553535')
        CustomerProfile.objects.create(customer=self.user)
        self.url = reverse('profile')

    def test_get_personal_profile_page_when_not_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_personal_profile_when_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_personal_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data={'city': 'Иркутск'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.customer_profile.city, 'Иркутск')


class TestTokenAuthenticationSystem(APITestCase):

    def setUp(self) -> None:
        self.url_register = reverse('register')
        self.url_personal_profile = reverse('profile')
        self.url_token_auth = reverse('api_token_auth')

    def test_obtain_token_when_email_is_not_confirmed(self):
        """
        When user's account is created, but his email is_active=False,
        he is not supposed to obtain token. Only when he makes his account active,
        he obtain it.
        """
        response = self.client.post(self.url_register, data={'user_name': 'testuser1', 'email': 'testuser1@gmail.com',
                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser1')

    def test_login_with_token_when_email_is_not_confirmed(self):
        """
        Here user is trying to login via token, but his email is not confirmed.
        He is not supposed to login.
        """
        response = self.client.post(self.url_register, data={'user_name': 'testuser1', 'email': 'testuser1@gmail.com',
                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser1')
        response = self.client.post(self.url_token_auth, data={'username': 'testuser1', 'password': 'pWrDLoL1#3!'})
        token = (eval(response.content.decode()).get('token'))

        headers = {'content-type': 'application/json', 'Authorization': f'Token {token}'}
        response = self.client.get(self.url_personal_profile, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_token_when_email_is_confirmed(self):
        """
        Here user is trying to login via token, AND his email IS confirmed.
        He is supposed to login.
        """
        response = self.client.post(self.url_register, data={'user_name': 'testuser1', 'email': 'testuser1@gmail.com',
                                    'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})
        user = Customer.objects.get(user_name='testuser1')
        email_msg = mail.outbox[0]
        link = re.search(r'http://.+', email_msg.body).group()
        response = self.client.get(link, follow=True)
        user.refresh_from_db()

        response = self.client.post(self.url_token_auth, data={'username': 'testuser1', 'password': 'pWrDLoL1#3!'})
        token = (eval(response.content.decode()).get('token'))

        headers = {'content-type': 'application/json', 'Authorization': f'Token {token}'}
        response = self.client.get(self.url_personal_profile, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCustomerProfileCreated(APITestCase):

    def setUp(self) -> None:
        self.client.post(reverse('register'), data={'user_name': 'testuser1', 'email':'testuser3@gmail.com',
                         'password': 'pWrDLoL1#3!', 'password2': 'pWrDLoL1#3!'})

        self.user = Customer.objects.get(user_name='testuser1')
        self.customer_profile = self.user.customer_profile

    def test_personal_profile_automatically_created_after_customer_created(self):
        self.assertEqual(self.customer_profile.customer.user_name, self.user.user_name)

    def test_image_default(self):
        self.assertEqual(self.customer_profile.image_url, 'media/images.png')


class TestChangingEmail(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('change_email_view')

        self.user1 = Customer.objects.create_user(email='testmail1@gamil.com', user_name='testuser1', password='1234')
        self.user2 = Customer.objects.create_user(email='testmail2@gamil.com', user_name='testuser2', password='1234')
        self.email_to_change = 'emailcahnge@gmail.com'

    def test_response_status_code(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data={'email': self.email_to_change})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_email(self):
        self.client.force_authenticate(self.user1)
        self.client.post(self.url, data={'email': self.email_to_change})
        email_msg = mail.outbox
        self.assertNotEquals(email_msg, [])

    def confirm_email_change(self):
        self.client.force_authenticate(self.user1)
        self.client.post(self.url, data={'email': self.email_to_change})
        email_msg = mail.outbox[0]

        link = re.search(r'http://.+', email_msg.body).group()
        self.client.get(link, follow=True)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, self.email_to_change)

    def test_change_email_that_already_exists(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data={'email': self.user2.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        email_msg = mail.outbox
        self.assertEqual(email_msg, [])


class TestChangingUserName(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('change_username_view')

        self.user1 = Customer.objects.create_user(email='testmail1@gamil.com', user_name='testuser1', password='1234')
        self.user2 = Customer.objects.create_user(email='testmail2@gamil.com', user_name='testuser2', password='1234')
        self.username_to_change = 'usernamechange'

    def test_response_status_code(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data={'user_name': self.username_to_change})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_email(self):
        self.client.force_authenticate(self.user1)
        self.client.post(self.url, data={'user_name': self.username_to_change})
        email_msg = mail.outbox
        self.assertNotEquals(email_msg, [])

    def confirm_username_change(self):
        self.client.force_authenticate(self.user1)
        self.client.post(self.url, data={'email': self.username_to_change})
        email_msg = mail.outbox[0]

        link = re.search(r'http://.+', email_msg.body).group()
        self.client.get(link, follow=True)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.user_name, self.username_to_change)

    def test_change_email_that_already_exists(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, data={'username': self.user2.user_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        email_msg = mail.outbox
        self.assertEqual(email_msg, [])

