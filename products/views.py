from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from products.models import Product
from orders.models import Order, Cart
from .serializers import (
    ProductSerializer, 
    ProductDetailSerializer, 
    AddToCartSerializer, 
    BuyNowSerializer
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": "Invalid input.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        quantity = serializer.validated_data['quantity']

        # Check stock availability
        if quantity > product.stock:
            return Response({
                'status': 'error',
                'message': f'Cannot add more than {product.stock} items.'
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if not created:
                if cart_item.quantity + quantity > product.stock:
                     return Response({
                        'status': 'error',
                        'message': f'Cannot add more than {product.stock} items (including cart).'
                    }, status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

        return Response({
            "status": "success",
            "message": f"{product.name} added to cart.",
            "data": {
                "product": product.name,
                "quantity": cart_item.quantity
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def buy_now(request, product_id):
    serializer = BuyNowSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "message": "Invalid input.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        quantity = serializer.validated_data['quantity']

        # Validate stock
        if quantity > product.stock:
            return Response({
                "status": "error",
                "message": f"Insufficient stock. Available: {product.stock}."
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # create order (Order model save method handles stock deduction)
            total_price = product.price * quantity
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

        return Response({
            "status": "success",
            "message": f"You purchased {quantity} {product.name}.",
            "data": {
                "order_id": order.id,
                "total_price": str(total_price)
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def products(request):
    try:
        # Optimized query with select_related and prefetch_related
        instances = Product.objects.select_related('brand').prefetch_related('category').all().order_by('-created_at')
        serializer = ProductSerializer(instances, many=True, context={"request": request})

        return Response({
            "status": "success",
            "message": "Products retrieved successfully",
            "data": serializer.data
        }, status=HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def productdetail(request, pk):
    try:
        # Optimized query
        instance = get_object_or_404(
            Product.objects.select_related('brand', 'feature')
            .prefetch_related('category', 'galleries', 'colour', 'size'),
            pk=pk
        )
        serializer = ProductDetailSerializer(instance, context={"request": request})

        return Response({
            "status": "success",
            "message": "Product details retrieved successfully",
            "data": serializer.data
        }, status=HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)
