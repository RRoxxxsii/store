import json

from rest_framework.test import APITestCase
from django.test import RequestFactory

from store.models import Product, Brand, Category, Vendor, ProductImage
from store.serializers import ProductListSerializer, ProductDetailSerializer, CategoryListSerializer, \
    CategoryDetailSerializer


class FixtureTestData:

    def setUp(self) -> None:
        self.vendor = Vendor.objects.create(vendor_name='vendor', description='description')

        # Category
        self.category = Category.objects.create(category_name='category', description='description')

        self.category2 = Category.objects.create(category_name='category2', description='description')

        # Subcategory
        self.subcategory = Category.objects.create(category_name='subcategory', description='description',
                                                   parent_id=self.category.id)

        self.subcategory2 = Category.objects.create(category_name='subcategory2', description='description',
                                                   parent_id=self.category.id)

        self.subcategory3 = Category.objects.create(category_name='subcategory3', description='description',
                                                   parent_id=self.category2.id)

        # Brand
        self.brand = Brand.objects.create(brand_name='brand')

        # Products
        self.product1 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, vendor_id=self.vendor.id, category_id=self.subcategory.id,
                                               brand_id=self.brand.id,
                                               )

        self.product2 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=50, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )

        self.product3 = Product.objects.create(product_name='product', description='description', amount=50,
                                               price=50000, discount_percent=5, vendor_id=self.vendor.id,
                                               category_id=self.subcategory.id, brand_id=self.brand.id,
                                               )

        # Images
        ProductImage.objects.create(product_id=self.product1.id, is_feature=True, image='media/images.png')
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False)
        ProductImage.objects.create(product_id=self.product1.id, is_feature=False)

        ProductImage.objects.create(product_id=self.product3.id, is_feature=True)


class TestProductListSerializer(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.request = RequestFactory().get('/')

        self.data = ProductListSerializer((self.product1, self.product2, self.product3), many=True,
                                          context={'request': self.request}).data
        self.expected_data = [
            {
                'product_name': self.product1.product_name,
                'price': self.product1.price,
                'discount_percent': self.product1.discount_percent,
                'price_with_discount': self.product1.get_price_with_discount(),
                'product_image': [
                    {
                        "image_url": 'http://testserver' + str(self.product1.product_image.first().image.url),
                        "alt_text": None
                    }
                ]
            },
            {
                'product_name': self.product2.product_name,
                'price': self.product2.price,
                'discount_percent': self.product2.discount_percent,
                'price_with_discount': self.product2.get_price_with_discount(),
                'product_image': []
            },

            {
                'product_name': self.product3.product_name,
                'price': self.product3.price,
                'discount_percent': self.product3.discount_percent,
                'price_with_discount': self.product3.get_price_with_discount(),
                'product_image': [
                    {
                        "image_url": 'http://testserver' + str(self.product3.product_image.first().image.url),
                        "alt_text": None
                    }
                ]
            },
        ]

    def test_ok(self):
        data_json = json.dumps(self.data, indent=4, sort_keys=True)
        expected_data_json = json.dumps(self.expected_data, indent=4, sort_keys=True)

        self.assertEqual(data_json, expected_data_json)


class TestProductDetailSerializer(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.request = RequestFactory().get('/')

        self.data = ProductDetailSerializer(instance=self.product1, context={'request': self.request}).data
        self.data2 = ProductDetailSerializer(instance=self.product2, context={'request': self.request}).data
        self.data3 = ProductDetailSerializer(instance=self.product3, context={'request': self.request}).data

        expected_data = {
            "amount": 50,
            "brand": "Brand",
            "description": "description",
            "discount_percent": 0,
            "in_stock": False,
            "price": 50000,
            "price_with_discount": 50000,
            "product_image": [
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png"
                },
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png"
                },
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png"
                }
            ],
            "product_name": "Product",
            "vendor": "Vendor"
        }

        expected_data2 = {"amount": 50,
                               "brand": "Brand",
                               "description": "description",
                               "discount_percent": 50,
                               "in_stock": False,
                               "price": 50000,
                               "price_with_discount": 25000,
                               "product_image": [],
                               "product_name": "Product",
                               "vendor": "Vendor"
                               }

        expected_data3 = {
            "amount": 50,
            "brand": "Brand",
            "description": "description",
            "discount_percent": 5,
            "in_stock": False,
            "price": 50000,
            "price_with_discount": 47500,
            "product_image": [
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png"
                }
            ],
            "product_name": "Product",
            "vendor": "Vendor"
        }

        self.expected_data_json = json.dumps(expected_data, indent=4, sort_keys=True)
        self.expected_data_json2 = json.dumps(expected_data2, indent=4, sort_keys=True)
        self.expected_data_json3 = json.dumps(expected_data3, indent=4, sort_keys=True)


    def test_ok(self):
        data_json = json.dumps(self.data, indent=4, sort_keys=True)
        data_json2 = json.dumps(self.data2, indent=4, sort_keys=True)
        data_json3 = json.dumps(self.data3, indent=4, sort_keys=True)

        self.assertEqual(data_json, self.expected_data_json)
        self.assertEqual(data_json2, self.expected_data_json2)
        self.assertEqual(data_json3, self.expected_data_json3)


class TestCategoryListSerializer(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.request = RequestFactory().get('/')
        self.data = CategoryListSerializer(Category.objects.filter(parent__isnull=True), many=True,
                                            context={'request': self.request}).data

        expected_data = [
            {
                "category_name": "Category",
                "children": [
                    {
                        "category_name": "Subcategory",
                        "children": []
                    },
                    {
                        "category_name": "Subcategory2",
                        "children": []
                    }
                ]
            },
            {
                "category_name": "Category2",
                "children": [
                    {
                        "category_name": "Subcategory3",
                        "children": []
                    }
                ]
            }
        ]

        self.expected_data_json = json.dumps(expected_data, indent=4, sort_keys=True)

    def test_ok(self):
        data_json = json.dumps(self.data, indent=4, sort_keys=True)
        self.assertEqual(data_json, self.expected_data_json)

