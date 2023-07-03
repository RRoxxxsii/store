from django.urls import path
from . import views


urlpatterns = [
    # pk of a product and comments referred to the product
    path('opinion/<int:pk>/product/', views.ReviewByProductIDListAPIView.as_view(), name='review-by-prod'),
    path('opinion/<int:pk>/post/', views.ProductReviewPostAPIView.as_view(), name='product-detail-post'),

    # id of review
    path('opinion/<int:pk>/edit/', views.ProductReviewRetrieveUpdateDestroyView.as_view(), name='review-update'),

    # all comments
    path('opinion/', views.ProductReviewListAPIView.as_view(), name='review-list')
]



