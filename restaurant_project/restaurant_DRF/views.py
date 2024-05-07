from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from .serializers import MenuSerializer,CategorySerializer,BookingSerializer,RatingSerializer,GroupSerializer,CartSerializer,OrderItemSerializer,OrderSerializer
from restaurant_app.models import MenuItem,Category,Booking,Rating,Cart,Order,OrderItem
from rest_framework import status,generics,mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.exceptions import PermissionDenied
from .throttle import CustomRateThrottle
from .permissions import MenuItemPermittions,SpecificMenuItemPermittions,GroupManagementPermittions,DeleteUserFromGroupPermittions,CartManagementPermissions,OrderPermissions
from django.contrib.auth.models import User,Group
from django.core.exceptions import ObjectDoesNotExist
from .services import manage_user_group
from django.http import JsonResponse,Http404
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework import filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
# Pagination Class

class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Filter Class

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'user': ['exact'],
            'user__username': ['exact', 'icontains'],
        }
    
@api_view()
def menu_item(request):
    items = MenuItem.objects.all()
    serialized_item = MenuSerializer(items,many=True)
    return Response(serialized_item.data)



class MenuView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [MenuItemPermittions]
    
    
# class MenuItemView(generics.ListCreateAPIView):
class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [SpecificMenuItemPermittions]
    # lookup_field = 'name' # Using name instead of pk as expected parameter in url
    
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price','inventory']
    search_fields = ['title']

class Managers(generics.ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupManagementPermittions]
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                manage_user_group(user,'Manager',add=True)
                return Response({"message": f"User {username} added to Manager"},status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error":"Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)

class ManagersDelete(generics.DestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DeleteUserFromGroupPermittions]
    
    def delete(self, request, *args, **kwargs):
            try:
                user = self.get_object()
                # print (user)
                manage_user_group(user,'Manager',add=False)
                return Response({"message": f"User {user.username} removed from Manager"},status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error":"Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)
            
class DeliveryCrew(generics.ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupManagementPermittions]
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                manage_user_group(user,'Delivery Crew',add=True)
                return Response({"message": f"User {username} added to Delivery Crew"},status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error":"Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)

class DeliveryCrewDelete(generics.DestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DeleteUserFromGroupPermittions]
    
    def delete(self, request, *args, **kwargs):
            try:
                user = self.get_object()
                manage_user_group(user,'Delivery Crew',add=False)
                return Response({"message": f"User {user.username} removed from Delivery Crew"},status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error":"Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)
        

class OrderItemManagement(APIView):

    permission_classes = [OrderPermissions]
    # pagination_class = OrderPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = OrderFilter
    # ordering_fields = ['date','user']
    # ordering = ['date'] # Default ordering
    # # search_fields = ['user','user__username']
    
    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Manager").exists():
            order_item = Order.objects.all()
            serializer = OrderSerializer(order_item,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.user.groups.filter(name="Delivery Crew").exists():
            order_item = Order.objects.filter(delivery_crew_id=request.user.id)
            serializer = OrderSerializer(order_item,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            order_item = Order.objects.filter(user_id=request.user.id)
            serializer = OrderSerializer(order_item,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)  

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            cart_items = Cart.objects.filter(user=user)
            if not cart_items.exists():
                return JsonResponse({'error': f'User {user.username} currently logged in does not have a cart'}, status=404)
            
            order_total_price = 0
            order_obj = Order.objects.create(
                user=user,
                total_price=order_total_price,
                date=timezone.now().date()
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order_obj,
                    menu_item=item.menu_item,
                    quantity=item.quantity,
                    unity_price=item.unity_price,
                    total_price=item.total_price,
                )
                order_total_price += item.total_price
                item.delete()

            order_obj.total_price = order_total_price
            order_obj.save()
            
            return JsonResponse({'message': 'Carts created successfully'}, status=201)

        except Exception as e:
            print(f"error {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

class OrderItemManagementNew(APIView):
    
    permission_classes = [OrderPermissions]
    
    def get(self, request,pk, *args, **kwargs):
        order_items = OrderItem.objects.filter(order_id=pk)
        serializer = OrderItemSerializer(order_items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk):
        try:
            order = Order.objects.get(pk=pk)
            
            # Check if assigned user is from Delivery Crew Group
            delivery_crew_id = request.data.get('delivery_crew')
            delivery_crew_user = User.objects.get(id=delivery_crew_id)
            if not delivery_crew_user.groups.filter(name='Delivery Crew').exists():
                return Response({'Error':'User assigned wasn\'t Delivery Crew '})
        except Order.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        # Assign a new Delivery Crew and update status
        print(request.data.get('delivery_crew'))
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request':request})  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk, *args, **kwargs):
        
        obj_order = Order.objects.filter(id=pk).delete()
        return JsonResponse({'message':f'Order {pk} from  deleted succesfully'},status=200)
        
    
    
    
    
class CartManagement(APIView):

    permission_classes = [CartManagementPermissions]
    
    def get(self, request, *args, **kwargs):
        
        menu_item = Cart.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(menu_item,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
 
            
    def post(self, request, *args, **kwargs):
        user = request.user
        # Assuming the request data contains JSON with item details
        try:
            # data = json.loads(request.data)
            data = request.data
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        try:
            menu_item_id = data['menu_item_id']
            quantity = data.get('quantity',1)
        except KeyError:
            return JsonResponse({'error': 'Invalid data format. Required keys: menu_item_id'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return JsonResponse({'error': 'Menu item not found'},status=404)
        total_price = quantity * menu_item.price
        # Create new instance
        try:
            cart_item = Cart.objects.create(
                user=user,
                menu_item=menu_item,
                quantity=quantity,
                unity_price=menu_item.price,
                total_price=total_price,
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'message':f'Carts created for user {user.username} succesfully'},status=201)
    
    def delete(self,request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return JsonResponse({'message':f'Carts deleted from user {user.username} succesfully'},status=200)
    


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Rating view 

class RatingView(APIView):
    
    permission_classes = [IsAuthenticated] # blocks post and get for non authorized users
    throttle_classes = [CustomRateThrottle]
    def post(self, request):
        
        # if not request.user.is_authenticated:
        #     raise PermissionDenied("You must be logged in to post ratings.")
        
        existing_rating  = Rating.objects.filter(user=request.user, menuitem_id=request.data.get('menuitem_id')).first()
        if not existing_rating:
            serializer_class = RatingSerializer(data=request.data, context={'request':request})
        else:
            serializer_class = RatingSerializer(existing_rating)
            
            return Response({
                'message':f"User {request.user.username} already reviewd this item",
                'data': serializer_class.data}, status=status.HTTP_200_OK)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        queryset = Rating.objects.all()
        serializer_class = RatingSerializer(queryset, many=True)
        return Response(serializer_class.data,status=status.HTTP_200_OK)
    
class RatingViewList(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


    


# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     ordering_fields=['user']