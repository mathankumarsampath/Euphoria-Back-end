from django.urls import path
from .views import *  

urlpatterns = [
    path('user/wishlist/',wishlistView , name="user-wishlist"), 
    path('user/add_wishlist/', wishlist_toggle, name="user-add_wishlist"), 
    path('user/profile/', user_profile_view, name="user-profile"),
]
