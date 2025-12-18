from rest_framework import serializers
from .models import Category, Product, Review

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product']

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "category", "reviews", "rating"]