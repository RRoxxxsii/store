from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.CartAddAPIView.as_view(), name='add-to-cart'),
    path('summary/', views.CartSummaryAPIView.as_view(), name='cart-summary'),
    path('delete/', views.DeleteCartItemAPIView.as_view(), name='cart-item-delete'),
    path('update/', views.UpdateCartAPIView.as_view(), name='cart-update')
]




