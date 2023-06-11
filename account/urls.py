from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('register/', views.RegistrationAPIVIew.as_view(), name='register'),
    path('me/', views.ProfileAPIView.as_view(), name='profile'),
    path('confirm-email/', views.confirm_email_view, name='confirm_email_view'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]



