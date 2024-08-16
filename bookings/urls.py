from django.urls import path
from . import views

urlpatterns = [
    path('rules/', views.rules_view, name='rules_view'),  
    path('form/', views.booking_form, name='booking_form'),
    path('create/', views.create_booking, name='create_booking'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
]
