from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from products.models import Product
from orders.models import Order, Cart
from .serializers import ProductSerializer, ProductDetailSerializer 


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        quantity = int(request.data.get("quantity", 1))

        # Check stock availability
        if quantity <= 0 or quantity > product.stock:
            return Response({
                'status': 'error',
                'message': f'Cannot add more than {product.stock} items.'
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

        return Response({
            "status": "success",
            "message": f"{product.name} added to cart.",
            "quantity": cart_item.quantity
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def buy_now(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        quantity = int(request.data.get("quantity", 1))

        # Validate stock
        if quantity <= 0 or quantity > product.stock:
            return Response({
                "status": "error",
                "message": f"Insufficient stock. Available: {product.stock}."
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # reduce stock
            product.stock -= quantity
            product.save()

            # create order
            total_price = product.price * quantity
            Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

        return Response({
            "status": "success",
            "message": f"You purchased {quantity} {product.name}."
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def products(request):
    try:
        instances = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(instances, many=True, context={"request": request})

        return Response({
            "status_code": 200,
            "data": serializer.data
        }, status=HTTP_200_OK)

    except Exception as e:
        return Response({
            "status_code": 500,
            "error": str(e)
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def productdetail(request, pk):
    try:
        instance = get_object_or_404(
            Product.objects.select_related('brand', 'feature')
            .prefetch_related('category', 'galleries'),
            pk=pk
        )
        serializer = ProductDetailSerializer(instance, context={"request": request})

        return Response({
            "status_code": 200,
            "data": serializer.data
        }, status=HTTP_200_OK)

    except Exception as e:
        return Response({
            "status_code": 500,
            "error": str(e)
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)


