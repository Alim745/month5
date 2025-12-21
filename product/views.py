from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategoryListSerializer, CategoryDetailSerializer , ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer
from django.db.models import Avg
from .serializers import CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer

@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        list_ = CategoryListSerializer(categories, many=True).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'POST':
        print("Некорректные:", request.data)
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print("Исправленыые:", serializer.validated_data)

        name = serializer.validated_data.get('name')

        categorie = Category.objects.create(name=name)
        categorie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(categorie).data)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        categories = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"error": "Category not found!"})
    if request.method == 'GET':
        list_ = CategoryDetailSerializer(categories, many=False).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        categories.name = serializer.validated_data.get('name')
        categories.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(categories).data)
    elif request.method == 'DELETE':
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        list_ = ProductListSerializer(products, many=True).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    if request.method == 'GET':
        try:
            products = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "Category not found!"})
        list_ = ProductDetailSerializer(products, many=False).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        products = Product.objects.get(id=id)
        products.title = serializer.validated_data.get('title')
        products.description = serializer.validated_data.get('description')
        products.price = serializer.validated_data.get('price')
        products.category_id = serializer.validated_data.get('category_id')
        products.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(products).data)
    elif request.method == 'DELETE':
        products = Product.objects.get(id=id)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_crete_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewListSerializer(reviews, many=True).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        product_id = serializer.validated_data.get('product_id')
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')

        review = Review.objects.create(
            product_id=product_id,
            text=text,
            stars=stars
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    if request.method == 'GET':
        try:
            reviews = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "Category not found!"})
        list_ = ReviewDetailSerializer(reviews, many=False).data
        return Response(list_, status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():         
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        reviews = Review.objects.get(id=id)
        reviews.product_id = serializer.validated_data.get('product_id')
        reviews.text = serializer.validated_data.get('text')
        reviews.stars = serializer.validated_data.get('stars')
        reviews.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(reviews).data)
    elif request.method == 'DELETE':
        reviews = Review.objects.get(id=id)
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def products_with_reviews_api_view(request):
    products = Product.objects.all()
    for product in products:
        product.rating = sum(review.stars for review in product.reviews.all()) / product.reviews.count()

    list_ = ProductWithReviewsSerializer(products, many=True).data
    return Response(list_, status.HTTP_200_OK)