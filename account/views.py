from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.logic import UpdateEmail, Register, EmailConfirmationView, UpdateUserName
from account.models import Customer, EmailConfirmationToken
from account.permissions import IsNotAuthenticated
from account.serializers import RegisterSerializer, PersonalProfileSerializer, ChangeEmailSerializer, \
    ChangeUserNameSerializer, UserForgotPasswordSerializer, UserPasswordResetSerializer
from account.utils import send_confirmation_email


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalProfileSerializer

    def get_object(self):
        return self.request.user.customer_profile


class RegistrationAPIVIew(CreateAPIView):
    """
    Make user registered, but only when he is not authenticated
    """
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = Register(serializer)
            user = instance.create_user()
            instance.send_email_message('email/register_email.txt', user)
            data = {'message': 'На вашу почту пришло письмо, перейдите по ссылке в нем чтобы подтвердить аккаунт'}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)


class ChangeFieldAPIViewMixin(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ''
    update_class = ''
    template_name = ''
    success_msg = 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'
    error_msg = ''

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = self.update_class(serializer=serializer)
            if instance.unique():
                instance.send_email_message('change_email.txt', user=request.user)
                instance.set_to_session(request.session)
                return Response({'message': 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'}, status=200)
            return Response({'error': 'Пользователь с такой электронной почтой уже существует.'}, status=400)

        return Response(serializer.errors, status=400)


class ChangeEmailAPIView(ChangeFieldAPIViewMixin, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer
    update_class = UpdateEmail
    template_name = 'email/change_email.txt'
    error_msg = 'Пользователь с такой электронной почтой уже существует.'


class ChangeUserNameAPIView(ChangeFieldAPIViewMixin, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUserNameSerializer
    template_name = 'email/change_username.txt'
    update_class = UpdateUserName
    error_msg = 'Пользователь с такой электронной почтой уже существует.'


class ConfirmEmailView(EmailConfirmationView):
    success_message = 'Электронная почта успешно подтверждена.'
    error_message = 'Срок годности токена истек, запросите новый.'

    def get_confirmation_logic(self, user, request):
        user.is_active = True
        Token.objects.create(user=user)


class ConfirmEmailChangeViewMixin(EmailConfirmationView):
    success_message = ''
    error_message = ''
    # field of user model that is supposed to be changed
    new_data_field = ''

    def get_confirmation_logic(self, user, request):
        """
        Supposed to pop an item from session and assign it to user object in order to change a field.
        The field may be UserObj.email/UserObj.user_name
        """
        try:
            self.new_data_field = request.session.pop(self.new_data_field)
            user.email = self.new_data_field
        except KeyError:
            pass


class ConfirmEmailChangeView(ConfirmEmailChangeViewMixin, EmailConfirmationView):
    success_message = 'Электронная почта успешно обновлена.'
    error_message = 'Срок годности токена истек, запросите новый.'
    new_data_field = 'email'


class ConfirmEmailChangeUserNameView(ConfirmEmailChangeViewMixin, EmailConfirmationView):
    success_message = 'Имя пользователя успешно обновлено.'
    error_message = 'Срок годности токена истек, запросите новый.'
    new_data_field = 'user_name'





