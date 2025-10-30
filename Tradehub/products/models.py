from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="products")
    stock_quantity = models.PositiveBigIntegerField(default=0)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

        indexes = [models.Index(fields=["name"]),]


