from django.urls import path
from . import views 

urlpatterns = [

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('product/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('create-order/<str:pk>/', views.createOrder, name='create-order'),
    path('update-order/<str:pk>/', views.updateOrder, name='update-order'),
    path('delete-order/<str:pk>/', views.deleteOrder, name='delete-order'),




]