from django.urls import path

from . import views


urlpatterns = [
    path('add/', views.CartAddAPIView.as_view(), name='add-to-cart')
]




