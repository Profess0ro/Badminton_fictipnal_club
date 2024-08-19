from django.urls import path
from . import views

urlpatterns = [
    path('rules/', views.rules_view, name='rules_view'),
    path('form/', views.booking_view, name='booking_view'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
