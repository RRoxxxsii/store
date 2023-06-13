from abc import abstractmethod

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Customer, EmailConfirmationToken, CustomerProfile
from account.utils import send_confirmation_email
from account.models import Customer


class EmailConfirmMixin:
    def __init__(self, serializer):
        self.serializer = serializer

    def send_email_message(self, template_name: str, user: Customer):
        token = EmailConfirmationToken.objects.create(customer=user)
        send_confirmation_email(template_name, email=user.email, token_id=token.pk, user_id=user.pk)


class UpdateEmail(EmailConfirmMixin):

    def email_unique(self):
        new_email = self.serializer.validated_data['email']
        if Customer.objects.filter(email=new_email).exists():
            return False
        return True

    def set_email_to_session(self, session):
        session['new_email'] = self.serializer.validated_data['email']


class UpdateUserName(EmailConfirmMixin):
    def username_unique(self):
        user_name = self.serializer.validated_data['user_name']
        if Customer.objects.filter(user_name=user_name).exists():
            return False
        return True

    def set_username_to_session(self, session):
        session['new_username'] = self.serializer.validated_data['user_name']


class Register(EmailConfirmMixin):

    def create_user(self):
        mobile = self.serializer.data.get('mobile')
        if mobile == '':
            mobile = None
        user = Customer.objects.create_user(
            email=self.serializer.data.get('email'),
            mobile=mobile,
            user_name=self.serializer.data.get('user_name'),
            password=self.serializer.data.get('password'),
        )
        CustomerProfile.objects.create(customer=user)
        user.save()
        return user


class EmailConfirmationView(APIView):
    success_message = ''
    error_message = ''

    @abstractmethod
    def get_confirmation_logic(self, user: Customer, request: Request):
        pass

    def get(self, request: Request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)

        try:
            token = EmailConfirmationToken.objects.get(pk=token_id)
            user = token.customer
            self.get_confirmation_logic(user, request)
            user.save()
            return Response({'message': self.success_message}, status=200)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': self.error_message}, status=400)

