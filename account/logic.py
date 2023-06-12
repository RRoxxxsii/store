from account.models import Customer, EmailConfirmationToken, CustomerProfile
from account.utils import send_confirmation_email


class EmailConfirmMixin:
    def __init__(self, serializer):
        self.serializer = serializer

    def send_email_message(self, template_name: str, user):
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
