from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegistrationAPIVIew.as_view(), name='register'),
    path('me/', views.ProfileAPIView.as_view(), name='profile'),
    # path('send-confirmation-email/', views.SendEmailConfirmationTokenAPIView.as_view(),
    #      name='send_email_confirmation_api_view'),
    path('confirm-email/', views.confirm_email_view, name='confirm_email_view')
]



