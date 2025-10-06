from django.contrib import admin

from products.models import Gallery ,Product, Category, Brand, Size, Feature, Colour


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent_category"]
    
admin.site.register(Category, CategoryAdmin)

class GalleryAdmin(admin.TabularInline):
    list_display = ["product", "image"]
    model = Gallery

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "stock" , "name","brand", "price", ]
    
    inlines = [GalleryAdmin]
    
admin.site.register(Product, ProductAdmin)


admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Feature)

class ColurAdmin(admin.ModelAdmin):
    list_display = ["id", "colour"]
admin.site.register(Colour, ColurAdmin)

