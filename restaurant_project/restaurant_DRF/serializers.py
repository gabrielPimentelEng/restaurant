from rest_framework import serializers
from restaurant_app.models import Menu, Booking

class MenuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Menu
        fields = ['id','name','price','inventory']
        extra_kwargs = {
        'price':{'min_value':2},
        'inventory':{'min_value':0}
    }
        