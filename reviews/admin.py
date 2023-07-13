from django.contrib import admin

from .models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass

