from django.db import models
from django.contrib.auth.models import User#,Group
# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Menu(models.Model):
    name  = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.SmallIntegerField()
    description = models.CharField(max_length=1000,default="")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)

    def __str__(self):
        return self.name


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    
    class Meta:
        unique_together = ('user','menuitem_id')

    def __str__(self):
        return self.user
