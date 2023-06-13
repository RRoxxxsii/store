from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.logic import UpdateEmail, Register, EmailConfirmationView, UpdateUserName
from account.permissions import IsNotAuthenticated
from account.serializers import RegisterSerializer, PersonalProfileSerializer, ChangeEmailSerializer, \
    ChangeUserNameSerializer


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
            instance.send_email_message('register_email.txt', user)
            data = {'message': 'На вашу почту пришло письмо, перейдите по ссылке в нем чтобы подтвердить аккаунт'}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)


class ChangeEmailAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = UpdateEmail(serializer=serializer)
            if instance.email_unique():
                instance.send_email_message('change_email.txt', user=request.user)
                instance.set_email_to_session(request.session)
                return Response({'message': 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'}, status=200)
            return Response({'error': 'Пользователь с такой электронной почтой уже существует.'}, status=400)

        return Response(serializer.errors, status=400)


class ChangeUserNameAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUserNameSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = UpdateUserName(serializer=serializer)
            if instance.username_unique():
                instance.send_email_message('change_username.txt', user=request.user)
                instance.set_username_to_session(request.session)
                return Response({'message': 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'},
                                status=200)
            return Response({'error': 'Пользователь с такой именем уже существует.'}, status=400)

        return Response(serializer.errors, status=400)


class ConfirmEmailView(EmailConfirmationView):
    success_message = 'Электронная почта успешно подтверждена.'
    error_message = 'Срок годности токена истек, запросите новый.'

    def get_confirmation_logic(self, user, request):
        user.is_active = True
        Token.objects.create(user=user)


class ConfirmEmailChangeView(EmailConfirmationView):
    success_message = 'Электронная почта успешно обновлена.'
    error_message = 'Срок годности токена истек, запросите новый.'

    def get_confirmation_logic(self, user, request):
        try:
            new_email = request.session.pop('new_email')
            user.email = new_email
        except KeyError:
            pass


class ConfirmEmailChangeUserNameView(EmailConfirmationView):
    success_message = 'Имя пользователя успешно обновлено.'
    error_message = 'Срок годности токена истек, запросите новый.'

    def get_confirmation_logic(self, user, request):
        try:
            new_username = request.session.pop('new_username')
            user.user_name = new_username
        except KeyError:
            pass



