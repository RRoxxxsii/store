from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import EmailConfirmationToken, CustomerProfile
from account.permissions import IsNotAuthenticated
from account.serializers import RegisterSerializer, PersonalProfileSerializer


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


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.customer
        user.is_active = True
        Token.objects.create(user=user)
        user.save()
        data = {'is_active': True}
        return render(request, template_name='confirm_email_view.html', context=data)
    except EmailConfirmationToken.DoesNotExist:
        data = {'is_active': False}
        return render(request, template_name='confirm_email_view.html', context=data)





