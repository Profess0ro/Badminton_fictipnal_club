from django.contrib import admin
from .models import CourtType, Booking, StartTimes, EndTimes

admin.site.register(Booking)

admin.site.register(CourtType)

admin.site.register(StartTimes)

admin.site.register(EndTimes)
