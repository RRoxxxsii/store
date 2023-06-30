from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.ProductByCategoryAPIView.as_view(), name='category-detail')
]

router.register('products', views.ProductAPIViewSet)

urlpatterns += router.urls
