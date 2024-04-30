from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from .serializers import MenuSerializer,CategorySerializer,BookingSerializer
from restaurant_app.models import Menu,Category,Booking
from rest_framework import status,generics
from rest_framework.response import Response
# Create your views here.
# from rest_framework import generics,viewsets
# from .models import MenuItem, Category
# from .serializers import MenuItemSerializer, CategorySerializer
# from django_filters.rest_framework import DjangoFilterBackend

@api_view()
def menu_item(request):
    items = Menu.objects.all()
    serialized_item = MenuSerializer(items,many=True)
    return Response(serialized_item.data)



class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
# class MenuItemView(generics.ListCreateAPIView):
class MenuItemView(generics.RetrieveUpdateDestroyAPIView ):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    ordering_fields = ['price', 'inventory']
    # filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['price','inventory']
    search_fields = ['title']
    

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

