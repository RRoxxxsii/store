from django.urls import reverse
from rest_framework import serializers

from store.models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('image_url', 'alt_text', 'is_feature')
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
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'price', 'discount_percent', 'price_with_discount', 'detail_url')
        read_only = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_image'] = ProductImageSerializer(many=True, context=self.context,
                                                       instance=instance.product_image.filter(is_feature=True)).data
        return data

    def get_detail_url(self, instance):
        # Assuming you have a named URL pattern for the product detail view
        return self.context['request'].build_absolute_uri(reverse('product-detail', args=[instance.pk]))


class ProductDetailSerializer(SerializerDiscountPriceMixin):
    vendor = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('category', 'created', 'updated', 'send_email_created')
        read_only = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_image'] = ProductImageSerializer(many=True, context=self.context,
                                                       instance=instance.product_image.
                                                       filter(product_id=instance.id)).data
        return data


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('category_name', 'children', 'detail_url')

    def get_children(self, instance):
        subcategories = instance.children.all()
        serializer = self.__class__(subcategories, many=True,
                                    context=self.context)
        return serializer.data

    def get_detail_url(self, instance):
        if not instance.is_parent_category:
            return self.context['request'].build_absolute_uri(reverse('category-detail', args=[instance.slug]))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_parent_category:
            data.pop('detail_url', None)
        return data


class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        exclude = ('id',)
        read_only = True





