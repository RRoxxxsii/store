from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import CustomerProfile, Customer
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
    email = serializers.EmailField()


class ChangeUserNameSerializer(serializers.Serializer):
    user_name = serializers.CharField()

