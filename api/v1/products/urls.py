from django.urls import path

from api.v1.products import views

urlpatterns = [
    path('products/', views.products),
    path('products/<int:pk>', views.productdetail )
]