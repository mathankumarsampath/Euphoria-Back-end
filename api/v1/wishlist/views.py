from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from wishlist.models import Wishlist
from api.v1.wishlist.serializers import WishlistSerializer, UserSerializer

from products.models import Product  



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])  
def wishlistView(request):
    
    user = request.user
    instances = Wishlist.objects.filter(user=user)
    
    if not instances.exists():
        return Response({"status_code": 404, "message": "No wishlists found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WishlistSerializer(instances, many=True, context={"request": request} )
    
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)
 
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def wishlist_toggle(request):
    
    user = request.user
    product_id = request.data.get('product')

    if not product_id:
        return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": f"Product with id {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the product is already in the wishlist
    wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()  # Remove the product from the wishlist
        return Response({"message": "Product removed from your wishlist successfully."}, status=status.HTTP_204_NO_CONTENT)
    else:
        Wishlist.objects.create(user=user, product=product)  # Add the product to the wishlist
        return Response({"message": "Product added to your wishlist successfully."}, status=status.HTTP_201_CREATED)

        
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    
    user = request.user
    serializer = UserSerializer(user)  
    
    return Response(serializer.data)