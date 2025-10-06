from django.contrib import admin

from wishlist.models import Wishlist




class WishlistaAdmin(admin.ModelAdmin):
    list_display = ["user","product", "created_at"]
    list_filter=["user"]
    search_fields = ["product"]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs

        return qs.filter(user=self.request.user)    
admin.site.register(Wishlist, WishlistaAdmin)