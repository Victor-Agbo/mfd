from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    def __str__(self) -> str:
        return self.username
    cart = models.ManyToManyField("Product")

class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=64)
    


class Product(models.Model):
    def __str__(self) -> str:
        return self.name
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=16)
    img = models.CharField(max_length=512)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class Order(models.Model):
    def __str__(self) -> str:
        return f"{self.user} -> {self.product}"
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.DecimalField(blank=False, decimal_places=0, max_digits=16, default=1)
    #status