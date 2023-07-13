from django.contrib import admin

from .models import Brand, Category, Product, ProductImage, Vendor


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["category_name", ]}


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["brand_name", ]}

