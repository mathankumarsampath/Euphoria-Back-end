import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer

# Initialize logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """Handles user registration"""
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"User registered: {user.username}")
        
        return Response(
            {
                "status": "success",
                "message": "User registered successfully.",
                "data": {
                    "username": user.username,
                    "email": user.email
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    logger.error(f"Registration failed: {serializer.errors}")
    return Response(
        {
            "status": "error",
            "message": "Registration failed.",
            "errors": serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Handles user login and token generation"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        # User is already authenticated in serializer
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        logger.info(f"User logged in: {user.username}")
        
        return Response(
            {
                'status': 'success',
                'message': 'Login successful',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            status=status.HTTP_200_OK
        )
    
    logger.warning(f"Invalid login attempt: {serializer.errors}")
    return Response(
        {
            "status": "error", 
            "message": "Invalid credentials or inactive account.",
            "errors": serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )
