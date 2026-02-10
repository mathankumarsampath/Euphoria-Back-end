from django.urls import path

from products import views

urlpatterns = [
    path('products/', views.products),
    path('products/<int:pk>', views.productdetail ),
    path('add-to-cart/<int:product_id>/', views.add_to_cart , name='add-to-cart'),
    path('buy-now/<int:product_id>/', views.buy_now , name='buy-now')
]
