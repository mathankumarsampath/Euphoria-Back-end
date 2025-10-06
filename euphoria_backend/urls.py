from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include


print("URL Routing Initialized...")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/v1/', include('api.v1.products.urls')),
    path('api/v1/wishlist/', include('api.v1.wishlist.urls')),
    path('user/', include('orders.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)