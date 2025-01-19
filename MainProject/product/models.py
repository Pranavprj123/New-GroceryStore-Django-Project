from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICE = (
    ('Vegetable & Fruits','Vegetable & Fruits'),
    ('FoodGrains & Oil', 'FoodGrains & Oil'),
    ('DairyProducts', 'DairyProducts'),
    ('Chicken & Meat', 'Chicken & Meat'),
    
)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=18)
    image = models.ImageField(upload_to='products/')
    

    def __str__(self):
        return f'{self.name}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    

    # Below Property will be used by checkout.html page to show total cost in order summary
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    
#REVIEW - Extra

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} wishes for {self.product.name}'
