from django.db import models

# Create your models here.



class Menu(models.Model):
    name  = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.name


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name