from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from .serializers import MenuSerializer
from restaurant_app.models import Menu
from rest_framework import status,generics
from rest_framework.response import Response
# Create your views here.


@api_view()
def menu_item(request):
    items = Menu.objects.all()
    serialized_item = MenuSerializer(items,many=True)
    return Response(serialized_item.data)



class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
class MenuItemView(generics.RetrieveUpdateDestroyAPIView ):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer