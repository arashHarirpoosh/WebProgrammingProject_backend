from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.


class StoreUser(User):
    # pass
    address = models.CharField(max_length=1024)
    balance = models.FloatField()


# Category Table
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    categoryName = models.CharField(default='دسته بندی نشده', max_length=512, blank=False)


# Product table
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    productName = models.CharField(max_length=512)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    numberOfProducts = models.IntegerField()
    numberOfPurchased = models.IntegerField()
