from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



urlpatterns = [
    # path('menu',views.menu_item, name='menu-drf'),
    path('menu-items',views.MenuView.as_view(), name='menu-item'),
    # path('menu-items/<str:name>',views.MenuItemView.as_view(), name='menu-item'),
    path('menu-items/<int:pk>',views.MenuItemView.as_view(), name='menu-item'),
    path('category', views.CategoriesView.as_view()),
    path('book', views.BookingView.as_view()),
    path('book/<int:pk>', views.BookingDeleteView.as_view()),
    path('rating', views.RatingView.as_view()),
    path('rating-create/<int:pk>', views.RatingViewList.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
