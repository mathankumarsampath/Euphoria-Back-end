from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product, Brand, Category
from orders.models import Cart, Order
from django.urls import reverse
from django.contrib.auth.models import User

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        
        self.brand = Brand.objects.create(name="Nike")
        self.category = Category.objects.create(name="Shoes")
        self.product = Product.objects.create(
             name="Air Max",
             brand=self.brand,
             price=100.00,
             stock=10,
             rating=5
        )
        self.product.category.add(self.category)

    def test_products_list_query_count(self):
        # Create more products to verify N+1
        for i in range(10):
             p = Product.objects.create(
                 name=f"Shoe {i}", brand=self.brand, price=50, stock=5, rating=4
             )
             p.category.add(self.category)
        
        from django.test.utils import CaptureQueriesContext
        from django.db import connection
        
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get("/api/v1/products/")
            self.assertEqual(response.status_code, 200)
        
        # Expected: ~3-5 queries. If N+1, it would be > 12.
        print(f"DEBUG: Number of queries: {len(ctx)}")
        self.assertLess(len(ctx), 8)

    def test_add_to_cart_valid(self):
        url = reverse('add-to-cart', args=[self.product.id])
        data = {"quantity": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        
        cart = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart.quantity, 2)

    def test_add_to_cart_insufficient_stock(self):
        url = reverse('add-to-cart', args=[self.product.id])
        data = {"quantity": 11} # Stock is 10
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        # Check for status error in response
        self.assertEqual(response.data['status'], 'error')

    def test_add_to_cart_invalid_input(self):
        url = reverse('add-to-cart', args=[self.product.id])
        data = {"quantity": 0} 
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        
    def test_buy_now_stock_reduction(self):
        print(f"DEBUG: Initial Stock: {self.product.stock}")
        url = reverse('buy-now', args=[self.product.id])
        data = {"quantity": 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        self.product.refresh_from_db()
        print(f"DEBUG: Stock after purchase: {self.product.stock}")
        self.assertEqual(self.product.stock, 5) # 10 - 5
        
        order = Order.objects.filter(user=self.user, product=self.product).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.quantity, 5)
