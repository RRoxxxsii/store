from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination

from store.serializers import ProductDetailSerializer, ProductListSerializer


class ProductBaseMixin:
    serializer_class = ProductListSerializer
    serializer_detail_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_detail_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        products_cache_name = 'products_cache'
        products_cache = cache.get(products_cache_name)
        if products_cache:
            self.queryset = products_cache
        else:
            self.queryset = self.get_queryset()
            cache.set(products_cache_name, self.queryset, 600)
        return response


class ProductAPIPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 40



