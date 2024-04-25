from django.urls import path
from . import views




urlpatterns = [
    # path('menu',views.menu_item, name='menu-drf'),
    path('menu',views.MenuView.as_view(), name='menu-item'),
    path('menu-item/<int:pk>',views.MenuItemView.as_view(), name='menu-item'),
]
