from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Return the username as a string
    product = serializers.StringRelatedField()  # Return the product name as a string

    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'total_price', 'date_ordered']
