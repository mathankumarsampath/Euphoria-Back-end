from django.urls import path
from wishlist import views

urlpatterns = [
    path('user/wishlist/', views.wishlistView , name="user-wishlist"), 
    path('user/add_wishlist/', views.wishlist_toggle, name="user-add_wishlist"), 
    path('user/profile/', views.user_profile_view, name="user-profile"),
]
