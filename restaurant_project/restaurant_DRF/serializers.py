from rest_framework import serializers
from restaurant_app.models import MenuItem, Booking,Category,Rating
from django.contrib.auth.models import User,Group


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
        model = MenuItem
        fields = ['id','name','price','inventory','featured','category_id','category']
        extra_kwargs = {
        'price':{'min_value':2},
        'inventory':{'min_value':0}
    }

class GroupSerializer(serializers.ModelSerializer):
    
    group_names = serializers.SerializerMethodField()
    
    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]
            
            
    class Meta:
        model = User
        fields = ['id','username','group_names']
        extra_kwargs = {
            'username': {'validators': []},  # There was an auto validation that was preventing creation of new User (it was not being created)
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
    






