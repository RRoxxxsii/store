from django.urls import path

from notifications import views

urlpatterns = [
    path('subscribe-on-email/', views.SubscribeOnMailListingAPIView.as_view(), name='mail_listing_subscribe')
]

