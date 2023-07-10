from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **kwargs)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError('Необходимо ввести почтовый адрес')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=True,
                              validators=[RegexValidator(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')])

    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return self.user_name


class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customer_profile')
    city = models.CharField(max_length=250, default=None, null=True)
    image_url = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, default='media/images.png')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателя'


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

