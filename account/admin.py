from django.contrib import admin

from .models import Customer, CustomerProfile, EmailConfirmationToken


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfirmationToken)
class EmailConfirmationTokenAdmin(admin.ModelAdmin):
    pass
