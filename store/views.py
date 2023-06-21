from rest_framework.viewsets import ReadOnlyModelViewSet

from store.models import Product, Category
from store.serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer, CategoryDetailSerializer


class ProductAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    serializer_detail_class = ProductDetailSerializer
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_detail_class


class CategoryAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    serializer_detail_class = CategoryDetailSerializer
    queryset = Category.objects.filter(parent__isnull=True)
    queryset_detail = Category.objects.filter(parent__isnull=False)

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_detail_class

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset
        return self.queryset_detail




