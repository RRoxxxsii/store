from rest_framework.test import APITestCase


class TestProductListAPIView(APITestCase):

    def setUp(self) -> None:
        pass

    def test_product_list_get_request(self):
        pass

    def test_product_list_post_request(self):
        """
        Post request is not allower
        """
        pass


class TestProductRetrieveAPIView(APITestCase):

    def setUp(self) -> None:
        pass

    def test_product_detail_get_request(self):
        pass

    def test_product_detail_post_request(self):
        pass

    def test_product_does_not_exist(self):
        """
        Return HTTP_NOT_FOUND response.status_code
        """

class TestCategoryListAPIView(APITestCase):

    def setUp(self) -> None:
        pass

    def get_category_list(self):
        pass


class TestCategoryDetailView(APITestCase):

    def setUp(self) -> None:
        pass

    def test_get_parent_category(self):
        """
        Parent category is not supposed to be reachable. Response status code must be 400.
        """
        pass

    def test_get_subcategory(self):
        """
        Only subcategory is supposed to be reachable
        """
        pass





