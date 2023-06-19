from rest_framework.test import APITestCase
from store.models import Vendor, Product, Category, ProductImage, Brand


class TestDiscount(APITestCase):

    def setUp(self) -> None:
        # Vendor
        Vendor.objects.create(vendor_name='vendor', description='description')

        # Category
        self.category = Category.objects.create(category_name='category', description='description')

        # Subcategory
        self.subcategory = Category.objects.create(category_name='subcategory', description='description', parent_id=1)

        # Brand
        Brand.objects.create(brand_name='brand')

        # Image
        ProductImage.objects.create(image_url='media/images.png')

        # Products

        self.product1 = Product.objects.create(product_name='product', description='description', amount=50, price=50000,
                                               vendor_id=1, category_id=2, brand_id=1, image_id=1)

        self.product2 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=50,
                                               vendor_id=1, category_id=2, brand_id=1, image_id=1)

        self.product3 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=5,
                                               vendor_id=1, category_id=2, brand_id=1, image_id=1)

    def test_calculate(self):
        self.assertEqual(self.product1.get_price_with_discount(), 50000)
        self.assertEqual(self.product2.get_price_with_discount(), 25000)
        self.assertEqual(self.product3.get_price_with_discount(), 47500)

