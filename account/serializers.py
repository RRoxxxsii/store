from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.core.signals import request_finished

from .models import CustomerProfile, Customer, EmailConfirmationToken
from .signals import create_user_profile
from .utils import send_confirmation_email
from .validators import password_validate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[password_validate])
    password2 = serializers.CharField(validators=[password_validate])

    class Meta:
        model = Customer
        fields = ('user_name', 'email', 'mobile', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Пароли не совпадают."})

        return attrs

    def create(self, validated_data):
        mobile = validated_data.get('mobile')
        if mobile == '':
            mobile = None
        user = Customer.objects.create_user(
            email=validated_data['email'],
            mobile=mobile,
            user_name=validated_data['user_name'],
            password=validated_data['password'],
        )
        user.set_password(validated_data['password'])

        token = EmailConfirmationToken.objects.create(customer=user)
        send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)

        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('user_name', 'email', 'mobile')


class PersonalProfileSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ('city', 'customer', 'image_url')


class ConfirmationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

