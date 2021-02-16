from django.contrib import admin
from django.urls import path
from .views import sign_in,sign_up,customer_dash,logout,admin_dash
urlpatterns = [
    path('',sign_in,name="index"),
    path('register/',sign_up,name="signup"),
    path('customer/',customer_dash,name="customer"),
    path('logout/',logout,name="logout"),
    path('admin_dash/',admin_dash,name="admin_dash"),
]