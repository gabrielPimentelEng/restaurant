from rest_framework import serializers
from restaurant_app.models import MenuItem, Booking,Category,Rating,Cart,Order,OrderItem
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
        
class CartSerializer(serializers.ModelSerializer):
    
    item = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['user','username','menu_item_id','item','quantity','unity_price','total_price']
        
    def get_item(self,obj):
        return obj.menu_item.name
    def get_username(self,obj):
        return obj.user.username
    
class OrderItemSerializer(serializers.ModelSerializer):
    
    item = serializers.SerializerMethodField()
    order_owner = serializers.SerializerMethodField()
    delivery_crew_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id','order','order_owner','delivery_crew_name','menu_item_id','item','quantity','unity_price','total_price']
        
    def get_item(self,obj):
        return obj.menu_item.name
    def get_order_owner(self,obj):
        return obj.order.user.username
    def get_delivery_crew_name(self,obj):
        try:
            return obj.order.delivery_crew.username
        except AttributeError:
            return "Not assigned yet"
        
    
    
class OrderSerializer(serializers.ModelSerializer):
    
    # item = serializers.SerializerMethodField()
    # username = serializers.SerializerMethodField()
    order_owner = serializers.SerializerMethodField()
    delivery_crew_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','user','order_owner','delivery_crew','delivery_crew_name','status','total_price','date']
        
    def update(self,obj,validated_data):
        user = self.context['request'].user
        
        if user.groups.filter(name='Manager').exists():
            
            obj.delivery_crew = validated_data.get('delivery_crew',obj.delivery_crew)
            obj.status = validated_data.get('status',obj.status)
            obj.save()
        elif user.groups.filter(name='Delivery Crew').exists():
            obj.status = validated_data.get('status',obj.status)
            obj.save()
        return obj
    def get_delivery_crew_name(self,obj):
        try:
            return obj.delivery_crew.username
        except AttributeError:
            return "Not assigned yet"
    def get_order_owner(self,obj):
        return obj.user.username
    
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
    






