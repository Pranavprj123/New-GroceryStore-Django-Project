from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
    ('Maharashtra', 'Maharashtra'),
    ('Gujarat', 'Gujarat'),
    ('Rajasthan', 'Rajasthan'),
    ('Karnataka', 'Karnataka'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Kerala', 'Kerala'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('West Bengal', 'West Bengal'),
    ('Bihar', 'Bihar'),
    ('Punjab', 'Punjab'),
    ('Haryana', 'Haryana'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Telangana', 'Telangana'),
    ('Odisha', 'Odisha'),
    ('Assam', 'Assam'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Jharkhand', 'Jharkhand'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
)



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)  
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    address = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=50,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.city}-{self.address}'

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"