from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('register/', views.RegistrationAPIVIew.as_view(), name='register'),
    path('me/', views.ProfileAPIView.as_view(), name='profile'),
    path('confirm-email/', views.confirm_email_view, name='confirm_email_view'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('change-email/', views.ChangeEmailAPIView.as_view(), name='change_email_view'),
    path('confirm-change-email/', views.confirm_email_change_view, name='confirm-email-change-view')

]



