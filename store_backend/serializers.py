from rest_framework import serializers
from store_backend.models import Product, Category, Receipt


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productName', 'category', 'price', 'numberOfProducts', 'numberOfPurchased')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category',)


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('productName', 'numOfPurchase', 'name', 'familyName', 'address', 'totalPrice',
                  'dateOfPurchase', 'trackingCode')
