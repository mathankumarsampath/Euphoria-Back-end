from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import Product, Feature, Category, Brand, Gallery
from orders.models import Order


        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id", "description"]

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "image"]
        

class FeatureSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = ["fabric", "pattern", "fit", "neck", "sleeves", "style"]
        
        
        
class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = [ "id", "image"]
        
class ProductSerializer(ModelSerializer):
    
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        fields =("id", "name", "image", "price","brand", "category", "created_at")
        model = Product
        
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    def get_brand(self, obj):
        return obj.brand.name if obj.brand else None
        
        
class ProductDetailSerializer(ModelSerializer):
    
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    feature = FeatureSerializer()
    galleries  = GallerySerializer(many=True, read_only=True)
    colour = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Product
        fields = ("id", "name", "image", "stock" ,"price", "category", "brand", "size", "description", "feature", "galleries", "colour", "rating" )
        
        
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    def get_brand(self, obj):
        return obj.brand.name if obj.brand else None
    
    def get_colour(self, obj):
        return [colour.colour for colour in obj.colour.all()]
    
    def get_size(self, obj):
        return [size.size for size in obj.size.all()]



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Return the username as a string
    product = serializers.StringRelatedField()  # Return the product name as a string

    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'total_price', 'date_ordered']
  