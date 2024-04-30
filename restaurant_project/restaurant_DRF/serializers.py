from rest_framework import serializers
from restaurant_app.models import Menu, Booking,Category,Rating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class MenuSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Menu
        fields = ['id','name','price','inventory','category_id','category']
        extra_kwargs = {
        'price':{'min_value':2},
        'inventory':{'min_value':0}
    }

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','user','menuitem_id','rating']

    






