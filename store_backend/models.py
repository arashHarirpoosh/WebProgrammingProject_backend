from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    address = models.CharField(max_length=1000)
    balance = models.FloatField(default=0)
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', unique=True, editable=False)
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS


# Category Table
class Category(models.Model):
    categoryName = models.CharField(default='دسته بندی نشده', max_length=512, unique=True, blank=False)


def default_category():
    return Category.objects.get_or_create(categoryName='دسته بندی نشده')


# Product table
class Product(models.Model):
    productName = models.CharField(max_length=512)
    productCategory = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='دسته بندی نشده')
    price = models.IntegerField()
    numberOfProducts = models.IntegerField()
    numberOfPurchased = models.IntegerField()


# Receipt table
class Receipt(models.Model):
    productName = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    numOfPurchase = models.IntegerField()
    name = models.CharField(max_length=512)
    familyName = models.CharField(max_length=512)
    address = models.CharField(max_length=1000)
    totalPrice = models.FloatField()
    dateOfPurchase = models.DateTimeField(auto_now_add=True, blank=True)
    trackingCode = models.IntegerField()


