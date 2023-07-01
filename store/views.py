from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from store.filters import ProductPriceFilterBackend
from store.models import Product, Category
from store.serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer


class ProductAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    serializer_detail_class = ProductDetailSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.OrderingFilter, ProductPriceFilterBackend]
    ordering_fields = ['price', 'product_name', 'created']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_detail_class


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProductByCategoryAPIView(APIView):

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        if not category or category.is_parent_category is True:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Страница не найдена"})

        products = Product.objects.filter(category__slug=slug, category__is_parent_category=False)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

