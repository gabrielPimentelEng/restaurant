from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from .serializers import MenuSerializer,CategorySerializer,BookingSerializer,RatingSerializer
from restaurant_app.models import Menu,Category,Booking,Rating
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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

# @api_view(['POST','DELETE'])
# @permission_classes([IsAdminUser])
# def managers(request):
#     user = request.data['user']
#     if user:
#         user = get_object_or_404(User, user=user)
#         managers = Group.objects.get(name="Manager")
#         if request.method == 'POST':
            
#             managers.user_set.add(user)
#         if request.method == 'DELETE':
#             managers.user_set.remove(user)
#         return Response({"message":"ok"})
    
#     return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

class RatingView(APIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def post(self, request):
        data = {"message":"POST request processed"}
        return Response(data,status=status.HTTP_200_OK)
    def get(self, request):
        queryset = Rating.objects.all()
        serializer_class = RatingSerializer
        data = {"message":"GET request processed"}
        return Response(data,status=status.HTTP_200_OK)
class RatingViewList(generics.ListCreateAPIView):
    
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
