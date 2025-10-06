from django.urls import path
from .views import AddToCartView, BuyNowView

urlpatterns = [
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('buy-now/<int:product_id>/', BuyNowView.as_view(), name='buy-now'),
]
