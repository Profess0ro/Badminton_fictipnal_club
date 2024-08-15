from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Booking
from django.utils import timezone
from django import forms
import datetime

class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'

class BookingCreateView(CreateView):
    model = Booking
    fields = ['court_type', 'booking_date']  
    widgets = {
        'booking_date': forms.SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year + 1)),
    }
    template_name = 'booking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Assuming today is the start of the day
        today = timezone.localdate()

        # Calculate the date 14 days from today
        future_date = today + timezone.timedelta(days=14)

        # Generate available time slots starting from 8:00 AM to 6:00 PM on the future_date
        available_slots = []
        for hour in range(8, 18):  # 8 AM to 6 PM
            for minute in [0]:  # Half-hour intervals
                slot_start = timezone.make_aware(timezone.datetime(future_date.year, future_date.month, future_date.day, hour, minute))
                if slot_start.time() >= timezone.now().time():  # Only add future slots
                    available_slots.append(slot_start)
        context['available_slots'] = available_slots

        return context

class BookingUpdateView(UpdateView):
    model = Booking
    fields = ['court_type', 'booking_date', 'time_slot', 'duration']
    template_name = 'booking_form.html'

class BookingDeleteView(DeleteView):
    model = Booking
    success_url = '/bookings/'
    template_name = 'booking_confirm_delete.html'
