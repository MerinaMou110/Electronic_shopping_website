from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    details = models.TextField()
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.title
