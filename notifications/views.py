from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Customer
from notifications.serializers import SubscribeOnMailListingSerializer


class SubscribeOnMailListingAPIView(APIView):

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = SubscribeOnMailListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.is_authenticated:
            user = Customer.objects.get(id=user.id)
            if user.on_mail_listing:
                user.on_mail_listing = False
            else:
                user.on_mail_listing = True
            user.save()
            return Response(status=status.HTTP_200_OK, data={"message": "You have successfully subscribed on"
                                                                        "email listing"})
        return Response(status=status.HTTP_401_UNAUTHORIZED)
