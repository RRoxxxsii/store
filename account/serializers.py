from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Customer, CustomerProfile
from .validators import password_validate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=35, required=True, validators=[password_validate])
    password2 = serializers.CharField(max_length=35, required=True, validators=[password_validate])

    class Meta:
        model = Customer
        fields = ('user_name', 'email', 'mobile', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Пароли не совпадают."})

        return attrs


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('user_name', 'email', 'mobile')


class PersonalProfileSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ('city', 'customer', 'image_url')


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ChangeUserNameSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)


class SubscribeOnMailListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('on_mail_listing',)

