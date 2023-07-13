from rest_framework.test import APITestCase

from .fixtures import FixtureTestData


class TestDiscount(FixtureTestData, APITestCase):

    def test_calculate(self):
        self.assertEqual(self.product1.get_price_with_discount(), 50000)
        self.assertEqual(self.product2.get_price_with_discount(), 25000)
        self.assertEqual(self.product3.get_price_with_discount(), 47500)

