from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.tests.fixtures import FixtureTestData


class TestReviewByProductID(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url_prod1 = reverse('review-by-prod', kwargs={'pk': self.product1.id})
        self.url_prod2 = reverse('review-by-prod', kwargs={'pk': self.product2.id})

    def test_get_response_status(self):
        response = self.client.get(self.url_prod1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductReviewList(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = reverse('review-list')

    def test_get_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductReviewPost(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url_prod1 = reverse('product-detail-post', kwargs={'pk': self.product1.id})
        self.url_prod2 = reverse('product-detail-post', kwargs={'pk': self.product2.id})

    def test_get_page_request_failed(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_prod1)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_request_not_authorized(self):
        response = self.client.post(self.url_prod1, data={'user': self.user1, 'product': self.product1, 'rating': 5,
                                                          'usage_period': 'LESS THAN MONTH', 'advantages': 'Quality',
                                                          'disadvantages': 'Price',
                                                          'comment': 'Not the best but not the worst'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_request_authorized(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url_prod1, data={'user': self.user1, 'product': self.product1, 'rating': 5,
                                                          'usage_period': 'LESS THAN MONTH', 'advantages': 'Quality',
                                                          'disadvantages': 'Price',
                                                          'comment': 'Not the best but not the worst'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestProductReviewRetrieveUpdateDestroy(FixtureTestData, APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = reverse('review-update', kwargs={'pk': self.product_review1.id})

    def test_get_request_review(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_update_review_not_authorized(self):
        response = self.client.post(self.url, data={'comment': 'NewComment'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_update_review_authorized(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.url, data={'comment': 'NewComment'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_review1.refresh_from_db()
        self.assertEqual(self.product_review1.comment, 'NewComment')

    def test_request_update_review_authorized_but_not_is_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.url, data={'comment': 'NewComment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product_review1.refresh_from_db()
        self.assertNotEquals(self.product_review1.comment, 'NewComment')

    def test_request_delete_review_authorized(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


