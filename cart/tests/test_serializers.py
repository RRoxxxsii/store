import json

from cart.serializers import CartSummarySerializer
from store.tests.fixtures import FixtureTestCartData
from rest_framework.test import APITestCase
from django.test import RequestFactory


class TestCartSummarySerializer(FixtureTestCartData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.request = RequestFactory().get('/')

        self.data = CartSummarySerializer([self.cart1], many=True, context={'request': self.request}).data

        self.expected_data = [
            {
                "product_amount": 5,
                "products": [
                    {
                        "detail_url": f"http://testserver/api/v1/store/products/{self.product1.id}/",
                        "discount_percent": self.product1.discount_percent,
                        "id": self.product1.id,
                        "price": self.product1.price,
                        "price_with_discount": self.product1.get_price_with_discount(),
                        "product_image": [
                            {
                                "alt_text": None,
                                "image_url": "http://testserver/media/images.png",
                                "is_feature": True
                            }
                        ],
                        "product_name": self.product1.product_name,
                    },
                    {
                        "detail_url": f"http://testserver/api/v1/store/products/{self.product2.id}/",
                        "discount_percent": self.product2.discount_percent,
                        "id": self.product2.id,
                        "price": self.product2.price,
                        "price_with_discount": self.product2.get_price_with_discount(),
                        "product_image": [],
                        "product_name": self.product2.product_name

                    },
                    {
                        "detail_url": f"http://testserver/api/v1/store/products/{self.product3.id}/",
                        "discount_percent": self.product3.discount_percent,
                        "id": self.product3.id,
                        "price": self.product3.price,
                        "price_with_discount": self.product3.get_price_with_discount(),
                        "product_image": [
                            {
                                "alt_text": None,
                                "image_url": "http://testserver/media/images.png",
                                "is_feature": True
                            }
                        ],
                        "product_name": self.product3.product_name,
                    }
                ],
                "total_price_with_discount": 122500,
                "total_regular_price": 150000
            }
        ]

    def test_ok(self):
        data_json = json.dumps(self.data, indent=4, sort_keys=True)
        expected_data_json = json.dumps(self.expected_data, indent=4, sort_keys=True)
        self.assertEqual(data_json, expected_data_json)