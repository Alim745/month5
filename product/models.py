from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(min_length=1, max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(min_length=1, max_length=250)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=1000)
    stars = models.IntegerField(min_value=1, max_value=5, default=5)
    
    def __str__(self):
        return f"Review {self.id}"