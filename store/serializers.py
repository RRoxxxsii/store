from rest_framework import serializers
from store.models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('image_url', 'alt_text',)
        editable = False
        read_only = True

    def get_image_url(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)


class SerializerDiscountPriceMixin(serializers.ModelSerializer):
    price_with_discount = serializers.SerializerMethodField()

    def get_price_with_discount(self, instance):
        return int(instance.price - instance.price / 100 * instance.discount_percent) if instance.discount_percent > 0 \
            else instance.price


class ProductListSerializer(SerializerDiscountPriceMixin):

    class Meta:
        model = Product
        fields = ('product_name', 'price', 'discount_percent', 'price_with_discount')
        read_only = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_image'] = ProductImageSerializer(many=True, context=self.context,
                                                       instance=instance.product_image.filter(is_feature=True)).data
        return data


class ProductDetailSerializer(SerializerDiscountPriceMixin):
    vendor = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('id', 'category')
        read_only = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_image'] = ProductImageSerializer(many=True, context=self.context,
                                                       instance=instance.product_image.
                                                       filter(product_id=instance.id)).data
        return data


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('category_name', 'children')

    def get_children(self, instance):
        subcategories = instance.children.all()
        serializer = CategoryListSerializer(subcategories, many=True)
        return serializer.data


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        exclude = ('id',)
        read_only = True



