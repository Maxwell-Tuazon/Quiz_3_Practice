from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.getRoutes, name='get-routes'),
    path('products/', views.getProducts, name='get-products'),
    path('users/profile/', views.getUserProfile, name='user-profile'),
    path('products/<str:pk>/', views.getProduct, name='get-product'),
]