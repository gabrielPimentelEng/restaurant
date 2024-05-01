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
    user_username = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id',read_only=True)
    class Meta:
        model = Rating
        fields = ['id','user_username','user_id','menuitem_id','rating']
        read_only_fields = ['user']
        extra_kwargs = {
            'rating': {'min_value': 0, 'max_value':5}
        }
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_user_username(self, obj):
        return obj.user.username if obj.user else None
    






