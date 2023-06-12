from account.models import Customer, EmailConfirmationToken
from account.utils import send_confirmation_email


class UpdateEmail:

    @staticmethod
    def email_unique(self):
        new_email = self.serializer.validated_data['email']
        if Customer.objects.filter(email=new_email).exists():
            return False
        return True

    @staticmethod
    def set_email_to_session(serializer, session):
        session['new_email'] = serializer.validated_data['email']

    @staticmethod
    def send_email_message(template_name: str, user):
        token = EmailConfirmationToken.objects.create(customer=user)

        send_confirmation_email(template_name, email=user.email, token_id=token.pk,
                                user_id=user.pk)


