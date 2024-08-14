from django.urls import path
from . import views
from .views import MyBookingsView, edit_booking, cancel_booking

urlpatterns = [
    path('make_booking/<int:court_id>/', views.make_booking, name='make_booking'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('booking/', views.booking_info, name='booking'),
    path('select_court/', views.select_court, name='select_court'),
    path('my_bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]