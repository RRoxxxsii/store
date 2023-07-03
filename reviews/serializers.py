from rest_framework import serializers

from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductReview
        fields = '__all__'


class ProductReviewPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        fields = ('rating', 'usage_period', 'advantages', 'disadvantages', 'comment')




