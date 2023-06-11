from django.db import IntegrityError
from rest_framework.test import APITestCase

from account.models import Customer


class TestCreateUser(APITestCase):

    def setUp(self) -> None:
        Customer.objects.create_user(user_name='testuser1', email='testuser1@gmail.com', password='somepswrd1',
                                     mobile='88005553535')

    def test_create_user(self):
        user1 = Customer.objects.create_user(user_name='testuser2', email='testuser2@gmail.com', password='somepswrd1',
                                             mobile='89086469507')
        self.assertEqual(user1.user_name, 'testuser2')
        self.assertEqual(user1.email, 'testuser2@gmail.com')
        self.assertEqual(user1.mobile, '89086469507')

    def test_create_user_without_email(self):
        try:
            Customer.objects.create_user(user_name='mishanya', password='somepswrd1')
        except TypeError:
            assert True
        else:
            assert False

    def test_create_user_without_username(self):
        try:
            Customer.objects.create_user(email='mishanya@gmail.com', password='somepswrd1')
        except TypeError:
            assert True
        else:
            assert False

    def test_create_user_with_email_that_already_exists(self):
        try:
            Customer.objects.create_user(user_name='testuser3', email='testuser1@gmail.com', password='somepswrd1')
        except IntegrityError:
            assert True
        else:
            assert False

    def test_create_user_with_name_that_already_exists(self):
        try:
            Customer.objects.create_user(user_name='testuser1', email='testuser3@gmail.com', password='somepswrd1')
        except IntegrityError:
            assert True
        else:
            assert False

    def test_create_user_with_mobile_that_already_exists(self):
        try:
            Customer.objects.create_user(user_name='testuser1', email='testuser3@gmail.com', password='somepswrd1',
                                         mobile='88005553535')
        except IntegrityError:
            assert True
        else:
            assert False


