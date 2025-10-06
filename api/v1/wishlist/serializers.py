from rest_framework import serializers
from wishlist.models import Wishlist
from products.models import Product  # Assuming Product model is here

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product']


class AddWishlistSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Wishlist
        fields = ['product']
        
    def create(self, validated_data):
        return Wishlist.objects.create(user=self.context['request'].user, **validated_data)
    
    def validate_product(self, value):
        if self.context['request'].user.is_authenticated:
            if Wishlist.objects.filter(user=self.context['request'].user, product=value).exists():
                raise serializers.ValidationError("Product already in wishlist.")
        return value
    
# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
