import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .fixtures import FixtureTestData


class TestProductListAPIView(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.product_list_url = reverse('product-list')

    def test_product_list_get_request(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_post_request(self):
        """
        Post request is not allowed
        """
        response = self.client.post(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestProductListAPIViewFilter(FixtureTestData, APITestCase):

    def setUp(self):
        super().setUp()

    def test_min_max_price(self):
        response = self.client.get('/api/v1/store/products/?min_price=100&max_price=10000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        amount_of_products = len(eval(str(json.loads(response.content.decode()))))
        self.assertEqual(amount_of_products, 2)

    def test_min_price(self):
        response = self.client.get('/api/v1/store/products/?min_price=49000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        amount_of_products = len(eval(str(json.loads(response.content.decode()))))
        self.assertEqual(amount_of_products, 3)

    def test_max_price(self):
        response = self.client.get('/api/v1/store/products/?max_price=20000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        amount_of_products = len(eval(str(json.loads(response.content.decode()))))
        self.assertEqual(amount_of_products, 2)

    def test_price_that_is_not_on_condition(self):
        response = self.client.get('/api/v1/store/products/?min_price=0&max_price=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        amount_of_products = len(eval(str(json.loads(response.content.decode()))))
        self.assertEqual(amount_of_products, 0)


class TestProductRetrieveAPIView(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.product_detail_url1 = reverse('product-detail', kwargs={'pk': self.product1.id})
        self.product_detail_url2 = reverse('product-detail', kwargs={'pk': self.product2.id})
        self.product_detail_url_does_not_exist = reverse('product-detail', kwargs={'pk': 10})

    def test_product_detail_get_request(self):
        response1 = self.client.get(self.product_detail_url1)
        response2 = self.client.get(self.product_detail_url2)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_product_detail_post_request(self):
        response = self.client.post(self.product_detail_url1)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_product_does_not_exist(self):
        """
        Return HTTP_NOT_FOUND response.status_code
        """
        response = self.client.get(self.product_detail_url_does_not_exist)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCategoryListAPIView(APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.category_list_url = reverse('categories')

    def test_get_category_list(self):
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_category_list(self):
        response = self.client.post(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestCategoryDetailView(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.parent_category_detail_url = reverse('category-detail', kwargs={'slug': self.category.slug})
        self.parent_category_detail_url2 = reverse('category-detail', kwargs={'slug': self.category2.slug})

        self.subcategory_detail_url = reverse('category-detail', kwargs={'slug': self.subcategory.slug})
        self.subcategory_detail_url = reverse('category-detail', kwargs={'slug': self.subcategory2.slug})

    def test_get_parent_category(self):
        """
        Parent category is not supposed to be reachable. Response status code must be 400.
        """
        response = self.client.get(self.parent_category_detail_url)
        response2 = self.client.get(self.parent_category_detail_url2)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_subcategory(self):
        """
        Only subcategory is supposed to be reachable
        """
        response = self.client.get(self.subcategory_detail_url)
        response2 = self.client.get(self.subcategory_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class TestProductsWithDiscount(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.product_list_url = reverse('products-with-discount-list')

    def test_products_with_discount_status_code(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_with_discount_amount(self):
        response = self.client.get(self.product_list_url)
        amount_of_products = len(eval(str(json.loads(response.content.decode()))))
        self.assertEqual(amount_of_products, 4)


