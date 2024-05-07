from django.db import models
from django.contrib.auth.models import User#,Group
# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    name  = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    inventory = models.SmallIntegerField()
    description = models.CharField(max_length=1000,default="")
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unity_price = models.DecimalField(max_digits=6,decimal_places=2)
    total_price = models.DecimalField(max_digits=6,decimal_places=2)
    class Meta:
        unique_together = ('menu_item','user')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status = models.BooleanField(db_index=True, default=0)
    total_price = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unity_price = models.DecimalField(max_digits=6,decimal_places=2)
    total_price = models.DecimalField(max_digits=6,decimal_places=2)
    class Meta:
        unique_together = ('order','menu_item')
  
    

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    
    class Meta:
        unique_together = ('user','menuitem_id')

    def __str__(self):
        return self.user
