from rest_framework import serializers

from account.models import Customer


class SubscribeOnMailListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('on_mail_listing',)
