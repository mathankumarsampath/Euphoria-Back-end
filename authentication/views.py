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
@permission_classes([permissions.AllowAny])  # Allow access to anyone (no auth required)
def register_view(request):
    """Handles user registration"""
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the user and generate JWT tokens
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        # Log registration
        logger.info(f"User registered: {user.username}")
        
        # Build URL dynamically based on request
        protocol = "http://" if not request.is_secure() else "https://"
        host = request.get_host()
        url = protocol + host + "/api/v1/auth/token"
        
        return Response(
            {
                "url": url,
                "status": "success",
                "message": "User registered successfully.",
                "data": serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    # Log registration failure
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
@permission_classes([permissions.AllowAny])  # Allow access to anyone (no auth required)
def login_view(request):
    """Handles user login and token generation"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'], 
            password=serializer.validated_data['password']
        )
        
        if user is not None and user.is_active:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Log login
            logger.info(f"User logged in: {user.username}")
            
            return Response(
                {
                    'status': 'success',
                    'message': 'Login successful',
                    'tokens': {
                        'refresh': refresh_token,
                        'access': access_token,
                    }
                },
                status=status.HTTP_200_OK
            )
        
        # Log invalid login attempt
        logger.warning(f"Invalid login attempt for username: {serializer.validated_data['username']}")
        return Response(
            {"status": "error", "message": "Invalid credentials or inactive account."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Log invalid input data
    logger.error(f"Invalid input data for login: {serializer.errors}")
    return Response(
        {
            "status": "error",
            "message": "Invalid input data.",
            "errors": serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )
