from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from account.logic import UpdateEmail
from account.models import EmailConfirmationToken, Customer
from account.permissions import IsNotAuthenticated
from account.serializers import RegisterSerializer, PersonalProfileSerializer, ChangeEmailSerializer
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
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.customer
        user.is_active = True
        Token.objects.create(user=user)
        user.save()
        return Response({'message': 'Электронная почта успешно подтверждена.'}, status=200)

    except EmailConfirmationToken.DoesNotExist:
        return Response({'message': 'Срок годности токена истек, запросите новый.'}, status=400)


class ChangeEmailAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if UpdateEmail.email_unique(serializer):
                UpdateEmail.send_email_message('change_email.txt', user=request.user)
                UpdateEmail.set_email_to_session(serializer, request.session)
                return Response({'message': 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'},
                                status=200)
            return Response({'error': 'Пользователь с такой электронной почтой уже существует.'}, status=400)

        return Response(serializer.errors, status=400)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def confirm_email_change_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)

    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.customer
        new_email = request.session.pop('new_email')
        user.email = new_email
        user.save()
        return Response({'message': 'Электронная почта успешно обновлена.'}, status=200)
    except EmailConfirmationToken.DoesNotExist:
        return Response({'error': 'Срок годности токена истек, запросите новый.'}, status=400)

