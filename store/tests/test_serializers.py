import json

from django.test import RequestFactory
from rest_framework.test import APITestCase

from store.models import Category
from store.serializers import (CategoryListSerializer, ProductDetailSerializer,
                               ProductListSerializer)

from .fixtures import FixtureTestData


class TestProductListSerializer(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.request = RequestFactory().get('/')

        self.data = ProductListSerializer((self.product1, self.product2, self.product3), many=True,
                                          context={'request': self.request}).data
        self.expected_data = [
            {
                'id': self.product1.id,
                'detail_url': f'http://testserver/api/v1/store/products/{self.product1.id}/',
                'discount_percent': self.product1.discount_percent,
                'price': self.product1.price,
                'price_with_discount': self.product1.get_price_with_discount(),
                'product_image': [
                    {
                        "image_url": 'http://testserver' + str(self.product1.product_image.first().image.url),
                        "alt_text": None,
                        "is_feature": True
                    }
                ],
                'product_name': self.product1.product_name
            },
            {
                'id': self.product2.id,
                'detail_url': f'http://testserver/api/v1/store/products/{self.product2.id}/',
                'discount_percent': self.product2.discount_percent,
                'price': self.product2.price,
                'price_with_discount': self.product2.get_price_with_discount(),
                'product_image': [],
                'product_name': self.product2.product_name,

            },

            {
                'id': self.product3.id,
                'detail_url': f'http://testserver/api/v1/store/products/{self.product3.id}/',
                'discount_percent': self.product3.discount_percent,
                'price': self.product3.price,
                'price_with_discount': self.product3.get_price_with_discount(),
                'product_image': [
                    {
                        "image_url": 'http://testserver' + str(self.product3.product_image.first().image.url),
                        "alt_text": None,
                        "is_feature": True
                    }
                ],
                'product_name': self.product3.product_name
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
            "id": self.product1.id,
            "in_stock": False,
            "price": 50000,
            "price_with_discount": 50000,
            "product_image": [
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png",
                    "is_feature": True
                },
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png",
                    "is_feature": False

                },
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png",
                    "is_feature": False

                }
            ],
            "product_name": "Product",
            "vendor": "Vendor"
        }

        expected_data2 = {"amount": 50,
                               "brand": "Brand",
                               "description": "description",
                               "discount_percent": 50,
                               "id": self.product2.id,
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
            "id": self.product3.id,
            "in_stock": False,
            "price": 50000,
            "price_with_discount": 47500,
            "product_image": [
                {
                    "alt_text": None,
                    "image_url": "http://testserver/media/images.png",
                    "is_feature": True
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
                        "children": [],
                        "detail_url": f'http://testserver/api/v1/store/categories/{self.subcategory.slug}/',
                    },
                    {
                        "category_name": "Subcategory2",
                        "children": [],
                        "detail_url": f'http://testserver/api/v1/store/categories/{self.subcategory2.slug}/',

                    }
                ]
            },
            {
                "category_name": "Category2",
                "children": [
                    {
                        "category_name": "Subcategory3",
                        "children": [],
                        "detail_url": f'http://testserver/api/v1/store/categories/{self.subcategory3.slug}/',

                    }
                ]
            }
        ]

        self.expected_data_json = json.dumps(expected_data, indent=4, sort_keys=True)

    def test_ok(self):
        data_json = json.dumps(self.data, indent=4, sort_keys=True)
        self.assertEqual(data_json, self.expected_data_json)

