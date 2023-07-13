from collections import OrderedDict

from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from account.serializers import RegisterSerializer


class TestRegisterSerializer(APITestCase):

    def setUp(self) -> None:
        user1 = {'email': 'testuser1@gmail.com', 'user_name': 'testuser1',
                 'password': 'testpswrd', 'mobile': '88005553535', 'password2': 'testpswrd'}
        user2 = {'email': 'testuser2@gmail.com', 'user_name': 'testuser2',
                 'password': 'testpswrd', 'mobile': '88005553536', 'password2': 'testpswrd'}
        user3 = {'email': 'testuser3@gmail.com', 'user_name': 'testuser3',
                 'password': 'testpswrd', 'mobile': '88005553537', 'password2': 'testpswrd'}
        user4 = {'email': 'testuser4@gmail.com', 'user_name': 'testuser4',
                 'password': 'testpswrd', 'password2': 'testpswrd'}

        self.serialized_data = RegisterSerializer([user1, user2, user3, user4], many=True).data

        self.expected_data = [
            OrderedDict(user_name="testuser1", email="testuser1@gmail.com", mobile="88005553535",
                        password="testpswrd", password2="testpswrd"),

            OrderedDict(user_name="testuser2", email="testuser2@gmail.com", mobile="88005553536",
                        password="testpswrd", password2="testpswrd"),

            OrderedDict(user_name="testuser3", email="testuser3@gmail.com", mobile="88005553537",
                        password="testpswrd", password2="testpswrd"),

            OrderedDict(user_name="testuser4", email="testuser4@gmail.com", mobile=None,
                        password="testpswrd", password2="testpswrd"),
        ]

    def test_serializer_correct(self):
        self.assertEqual(self.serialized_data, self.expected_data)


class TestRegisterSerializerPasswordsNotCorrect(APITestCase):

    def setUp(self) -> None:
        self.user1 = {'email': 'testuser1@gmail.com', 'user_name': 'testuser1',
                      'password': 'testpswrd@A1', 'mobile': '88005553535', 'password2': 'A@1anotherpswrd'}
        self.user2 = {'email': 'testuser2@gmail.com', 'user_name': 'testuser2',
                      'password': 'a!Ab8', 'mobile': '88005553536', 'password2': 'a!Ab8'}

        self.serializer1 = RegisterSerializer(data=self.user1)
        self.serializer2 = RegisterSerializer(data=self.user2)

    def test_two_passwords_dont_match(self):
        self.assertFalse(self.serializer1.is_valid())
        self.assertEqual(
            self.serializer1.errors,
            {'password': [ErrorDetail(string='Пароли не совпадают.', code='invalid')]}
        )

    def test_passwords_short(self):
        self.assertFalse(self.serializer2.is_valid())
        self.assertEqual(
            self.serializer2.errors,
            {'password': [ErrorDetail(string='Пароль должен быть не менее 8 символов', code='invalid')],
             'password2': [ErrorDetail(string='Пароль должен быть не менее 8 символов', code='invalid')]}
        )


