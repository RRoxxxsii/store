from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.logic import (ConfirmEmailChangeMixin, EmailConfirmationView,
                           Register, UpdateEmail, UpdateUserName)
from account.models import Customer
from account.permissions import IsNotAuthenticated
from account.serializers import (ChangeEmailSerializer,
                                 ChangeUserNameSerializer,
                                 PersonalProfileSerializer, RegisterSerializer, SubscribeOnMailListingSerializer)
from account.utils import ChangeFieldAPIViewMixin


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


class ConfirmEmailChangeView(ConfirmEmailChangeMixin, EmailConfirmationView):
    success_message = 'Электронная почта успешно обновлена.'
    error_message = 'Срок годности токена истек, запросите новый.'
    new_data_field = 'email'


class ConfirmEmailChangeUserNameView(ConfirmEmailChangeMixin, EmailConfirmationView):
    success_message = 'Имя пользователя успешно обновлено.'
    error_message = 'Срок годности токена истек, запросите новый.'
    new_data_field = 'user_name'



class SubscribeOnMailListingAPIView(APIView):

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = SubscribeOnMailListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.is_authenticated:
            user = Customer.objects.get(id=user.id)
            if user.on_mail_listing:
                user.on_mail_listing = False
            else:
                user.on_mail_listing = True
            user.save()
            return Response(status=status.HTTP_200_OK, data={"message": "You have successfully subscribed on"
                                                                        "email listing"})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


