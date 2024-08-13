from django.contrib import admin
from .models import Court, Booking

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    ordering = ['name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('court', 'start_time', 'end_time')
    ordering = ['-start_time']