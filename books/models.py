import email
from enum import Flag
from pickle import TRUE
from pickletools import read_uint1
from pyexpat import model
from statistics import mode
from sys import maxsize
from urllib.request import urlcleanup
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from jinja2 import ModuleLoader
from numpy import maximum
from zmq import DEALER
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Create your models here.



ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti Pay", "Khalti Pay"),
    
)


class Product(models.Model):
    product_id = models.AutoField
    Book_name = models.CharField(max_length=50)
    Author = models.CharField(max_length=50 , default='')
    genre = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, default="")
    price = models.IntegerField(default=0)
    pub_date = models.DateField(default=timezone.now)
    quantity = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(null=True,blank=TRUE, upload_to='books/images', default="")
    sequence = models.IntegerField(default=0)

# Define a string representation of the model, returning the name of the book
    def __str__(self):
        return self.Book_name
    
  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url='' # If the URL cannot be obtained, set it to an empty string
        return url
   

class Order(models.Model):
    user = models.CharField(max_length=20,null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS,default="Order Received")
    transaction_id = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    
    Book_name = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    

    @property
    def get_total(self):
        total = self.Book_name.price *self.quantity
        return total
    


class ShippingAddress(models.Model):
    City=(
    ('Kathmandu','Kathmandu'),
    ('Bhaktapur','Bhaktapur'),
    ('Lalitpur','Lalitpur'),)
    user = models.CharField(max_length=20,null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, null=True )
    city = models.CharField(max_length=100,choices=City, null=True )
    ward_no = models.IntegerField(null=True)
    zip_code = models.IntegerField(null=True)
    phone = models.IntegerField(blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)  # Star rating field

    def __str__(self):
        return self.user
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
        


class Wishlist(models.Model):
    user = models.CharField(max_length=20,null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

