from distutils.archive_util import make_zipfile
from itertools import product
from pyexpat import model
from turtle import title
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobilenumber = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)

CATAGORY_CHOICES =(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear')
)

STOCK_CHOICES = (
    ('In Stock','In Stock'),
    ('Out of Stock','Out of Stock'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description = models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATAGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    stock = models.CharField(choices=STOCK_CHOICES,default='In Stock',max_length=100)
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Canceled','Canceled')
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

RATING = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5')
)

class Comment(models.Model):
    product = models.ForeignKey(Product,related_name="comments" ,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=RATING,max_length=2)    
    def __str__(self):
        return '%s - %s' %(self.product.title,self.user_name)
    