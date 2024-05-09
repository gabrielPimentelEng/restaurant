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
from .throttle import AuthenticatedUserThrottle,UnauthenticatedUserThrottle
from .permissions import MenuItemPermittions,SpecificMenuItemPermittions,GroupManagementPermittions,DeleteUserFromGroupPermittions,CartManagementPermissions,OrderPermissions
from django.contrib.auth.models import User,Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError, FieldError
from .services import manage_user_group,apply_filters_and_pagination
from django.http import JsonResponse,Http404
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework import filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
import logging
# Pagination Class
from django.core.paginator import Paginator,EmptyPage


@api_view()
def menu_item(request):
    items = MenuItem.objects.all()
    serialized_item = MenuSerializer(items,many=True)
    return Response(serialized_item.data)

class MenuView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [MenuItemPermittions]
    filterset_fields = ['name','price']
    
    # def get(self, request, *args, **kwargs):
    #     # Dict to use custom keys for filtering
    #     filter_mappings = {
    #         'name__istartswith':'name',
    #         'price':'price',
    #         'featured':'featured'
    #     }
    #     # Apply custom filtering, default ordering and pagination
    #     filtered_paginated_items = apply_filters_and_pagination(self.get_queryset(), request, filter_mappings=filter_mappings)

    #     # Serialize the resulting queryset
    #     serializer = self.get_serializer(filtered_paginated_items, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    

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
                manage_user_group(user,'Manager',add=False)
                return Response({"message": f"User {user.username} removed from Manager"},status=status.HTTP_200_OK)
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
                return Response({"message": f"User {user.username} removed from Delivery Crew"},status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error":"Username {username} not found"}, status=status.HTTP_404_NOT_FOUND)
        

class OrderItemManagement(APIView):

    permission_classes = [OrderPermissions]
    
    def get(self, request, *args, **kwargs):
        if not request.user.groups.exists():
            order_item = Order.objects.filter(user_id=request.user.id)
        elif request.user.groups.filter(name="Manager").exists():
            order_item = Order.objects.all()
        elif request.user.groups.filter(name="Delivery Crew").exists():
            order_item = Order.objects.filter(delivery_crew_id=request.user.id)
 
        filter_mappings = {
            'date':'date',
            'status':'status'
        }
        # Apply custom filtering, default ordering and pagination
        filtered_paginated_orders = apply_filters_and_pagination(order_item,request, filter_mappings=filter_mappings)
        serializer = OrderSerializer(filtered_paginated_orders,many=True)
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

class OrderItemManagementSpecific(APIView):
    
    permission_classes = [OrderPermissions]
    
    def get(self, request, pk, *args, **kwargs):
        # Check if the user is part of a relevant group (assuming groups are used to determine customer status)
        if not request.user.groups.exists():
            # Retrieve all order items associated with the order_id 'pk'
            order_items = OrderItem.objects.filter(order_id=pk)
            # Ensure that the current user is authorized to view these order items
            if not order_items:
                return Response({'Error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            # Check if order items belong to the user making the request
            if any(item.order.user_id == request.user.id for item in order_items):
                filtered_paginated_orders = apply_filters_and_pagination(order_items, request)
                serializer = OrderItemSerializer(filtered_paginated_orders,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'Error': 'Not a Customer'}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self,request,pk):
        try:
            order = Order.objects.get(pk=pk)
            
            # Check if assigned user is from Delivery Crew Group
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id and not request.user.groups.filter(name='Manager').exists():
                return Response({'Error':'You do not have permittions to assign a Delivery Crew'})
            delivery_crew_user = User.objects.get(id=delivery_crew_id)
            if not delivery_crew_user.groups.filter(name='Delivery Crew').exists():
                return Response({'Error':'User assigned wasn\'t Delivery Crew '})
        except Order.DoesNotExist:
            return Response({'Error': 'Order not found for requested id'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"Error":"User not found for requested id"})
        # Assign a new Delivery Crew and update status
        print(request.data.get('delivery_crew'))
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request':request})  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk, *args, **kwargs):
        
        obj_order = Order.objects.filter(id=pk).delete()
        return JsonResponse({'Message':f'Order {pk} from  deleted succesfully'},status=status.HTTP_200_OK)
        
    
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
        return JsonResponse({'message':f'Carts deleted from user {user.username} succesfully'},status=status.HTTP_200_OK)

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
    
    def post(self, request):
        
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


class Test(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    # pagination_class = PageNumberPagination