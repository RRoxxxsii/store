from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [

]

router.register('products', views.ProductAPIViewSet)
router.register('categories', views.CategoryAPIViewSet)

urlpatterns += router.urls
