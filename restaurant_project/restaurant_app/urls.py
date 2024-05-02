from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('about/',views.about_view,name='about'),
    path('menu/',views.menu_view,name='menu'),
    path('book/',views.book_view,name='book'),
    path('book/',views.book_view,name='book'),
    path('booking_confirmation/',views.booking_confirmation, name ='book_submit'),
    path('menu/<int:pk>/',views.item_detail, name ='menu_item'),
    
    

]
