from django.db import models
from django.contrib.auth.models import User 
from products.models import Product



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Optional quantity tracking
    added_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValueError("Not enough stock aviliable")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tracks which user placed the order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Tracks which product was bought
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValueError("Not enough stock aviliable")
        self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.quantity} item(s)'
