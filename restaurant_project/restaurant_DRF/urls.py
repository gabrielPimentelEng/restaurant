from django.urls import path
from . import views




urlpatterns = [
    # path('menu',views.menu_item, name='menu-drf'),
    path('menu',views.MenuView.as_view(), name='menu-item'),
    path('menu/<int:pk>',views.MenuItemView.as_view(), name='menu-item'),
    path('category', views.CategoriesView.as_view()),
    path('book', views.BookingView.as_view()),
    path('book/<int:pk>', views.BookingDeleteView.as_view()),

]
