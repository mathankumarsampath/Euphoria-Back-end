
class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class BuyNowSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
