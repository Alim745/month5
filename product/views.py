from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategoryListSerializer, CategoryDetailSerializer , ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer
from django.db.models import Avg

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    list_ = CategoryListSerializer(categories, many=True).data
    return Response(list_, status.HTTP_200_OK)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        categories = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"error": "Category not found!"})
    list_ = CategoryDetailSerializer(categories, many=False).data
    return Response(list_, status.HTTP_200_OK)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    list_ = ProductListSerializer(products, many=True).data
    return Response(list_, status.HTTP_200_OK)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        products = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"error": "Category not found!"})
    list_ = ProductDetailSerializer(products, many=False).data
    return Response(list_, status.HTTP_200_OK)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewListSerializer(reviews, many=True).data
    return Response(list_, status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"error": "Category not found!"})
    list_ = ReviewDetailSerializer(reviews, many=False).data
    return Response(list_, status.HTTP_200_OK)



@api_view(['GET'])
def products_with_reviews_api_view(request):
    products = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def products_with_reviews_api_view(request):
    products = Product.objects.all()
    for product in products:
        product.rating = sum(review.stars for review in product.reviews.all()) / product.reviews.count()

    list_ = ProductWithReviewsSerializer(products, many=True).data
    return Response(list_, status.HTTP_200_OK)