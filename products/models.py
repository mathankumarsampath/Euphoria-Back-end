from django.db import models

# def get_default_feature():
#     feature, created = Feature.objects.get_or_create(
#         fabric="Cotton",
#         pattern="Solid",
#         fit="Regular",
#         neck="Round",
#         sleeves="Short",
#         style="Casual"
#     )
#     return feature


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_categories"
    )

    class Meta:
        db_table = "products_category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=16, unique=True)

    class Meta:
        db_table = "products_size"

    def __str__(self):
        return self.size


class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="products/images", blank=True, null=True)

    class Meta:
        db_table = "products_brand"

    def __str__(self):
        return self.name


class Feature(models.Model):
    fabric = models.CharField(max_length=128)
    pattern = models.CharField(max_length=128)
    fit = models.CharField(max_length=128)
    neck = models.CharField(max_length=128)
    sleeves = models.CharField(max_length=128)
    style = models.CharField(max_length=128)

    class Meta:
        db_table = "products_feature"

    def __str__(self):
        return self.fabric


class Gallery(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="galleries")
    image = models.ImageField(upload_to="products/images/")

    class Meta:
        db_table = "products_gallery"
        verbose_name_plural = "gallery"

    def __str__(self):
        return f"Gallery Image {self.id} for {self.product.name}"


class Colour(models.Model):
    colour = models.CharField()
    
    class Meta:
        db_table = "produts_colour"
        
    def __str__(self):
        return   f"Gallery Image {self.colour} "

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/images', blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    size = models.ManyToManyField(Size, related_name="products")
    colour = models.ManyToManyField(Colour, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = "products_product"

    def __str__(self):
        return self.name
