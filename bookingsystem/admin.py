from django.contrib import admin
from .models import CourtType, Booking

@admin.register(CourtType)
class CourtTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('court_type', 'booking_date', 'start_time', 'end_time')
    # Updated to use 'start_time' and 'end_time' instead of 'time_slot' and 'duration'
