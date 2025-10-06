from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from api.v1.products.serializers import ProductSerializer, ProductDetailSerializer
from products.models import Product


@api_view(["GET"])
@permission_classes([AllowAny])
def products(request):
    """Fetches all products ordered by the latest created date."""
    try:
        # Fetch all products ordered by the created_at date in descending order
        instances = Product.objects.all().order_by('-created_at')
        
        # Serialize the data
        context = {"request": request}
        serializer = ProductSerializer(instances, many=True, context=context)

        # Response data structure
        response_data = {
            "status_code": 200,
            "data": serializer.data
        }
        return Response(response_data, status=HTTP_200_OK)
    
    except Exception as e:
        # Return a more structured error response
        response_data = {
            "status_code": 500,
            "error": f"An error occurred while fetching products: {str(e)}"
        }
        return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def productdetail(request, pk):
    """Fetches product details by product id."""
    try:
        # Fetch the product by its primary key (pk)
        instance = get_object_or_404(
            Product.objects.select_related('brand', 'feature')
            .prefetch_related('category', 'galleries'),
            pk=pk
        )

        # Serialize the product details
        context = {"request": request}
        serializer = ProductDetailSerializer(instance, context=context)

        # Response data structure
        response_data = {
            "status_code": 200,
            "data": serializer.data
        }
        return Response(response_data, status=HTTP_200_OK)

    except Product.DoesNotExist:
        # Specific handling for product not found
        response_data = {
            "status_code": 404,
            "error": "Product not found"
        }
        return Response(response_data, status=HTTP_404_NOT_FOUND)

    except Exception as e:
        # Return a more structured error response for other exceptions
        response_data = {
            "status_code": 500,
            "error": f"An error occurred while fetching product details: {str(e)}"
        }
        return Response(response_data, status=HTTP_500_INTERNAL_SERVER_ERROR)
