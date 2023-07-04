from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import ProductReview
from reviews.permissions import IsOwner
from reviews.serializers import ProductReviewSerializer, ProductReviewPostSerializer
from store.models import Product


class ReviewByProductIDListAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        queryset = ProductReview.objects.filter(product=pk)

        serializer = ProductReviewSerializer(queryset, many=True, context={'request': request})

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProductReviewListAPIView(ListAPIView):
    queryset = ProductReview.objects.all().order_by('product_id')
    serializer_class = ProductReviewSerializer


class ProductReviewPostAPIView(APIView):
    serializer_class = ProductReviewPostSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                product = Product.objects.get(id=pk)
                review = serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Product.DoesNotExist:
                return Response({"error": "Товара не существует."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewPostSerializer
    queryset = ProductReview.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsOwner()]







