from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def send_confirmation_email(template_name: str, email: str, token_id: int, user_id: int):
    data = {
        'token_id': str(token_id),
        'user_id': str(user_id)
    }
    message = get_template(template_name).render(data)
    send_mail(subject='Пожалуйста, подтвердите почту',
              message=message,
              from_email='admin@ourweb.com',
              recipient_list=[email],
              fail_silently=True)

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
                instance.send_email_message('email/change_email.txt', user=request.user)
                instance.set_to_session(request.session)
                return Response({'message': 'Запрос на новую почту отправлен, перейдите по ссылке чтобы подтвердить.'}, status=200)
            return Response({'error': 'Пользователь с такой электронной почтой уже существует.'}, status=400)

        return Response(serializer.errors, status=400)



