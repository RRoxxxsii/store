from store.serializers import ProductListSerializer, ProductDetailSerializer


class ProductBaseMixin:
    serializer_class = ProductListSerializer
    serializer_detail_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.serializer_detail_class