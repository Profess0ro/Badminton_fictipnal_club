from django import forms
from .models import Booking
from django.utils import timezone
from datetime import timedelta

class BookingForm(forms.ModelForm):
    DURATION_CHOICES = [
        (1, '1 hour'),
        (2, '2 hours'),
    ]
    
    duration = forms.ChoiceField(choices=DURATION_CHOICES, label="Duration", initial=1)
    booking_time = forms.TimeField(label="Booking Time", widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = Booking
        fields = ['court', 'duration', 'booking_time']
        widgets = {
            'court': forms.HiddenInput(),  # Hide these fields in the form
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_time_str = cleaned_data.get('booking_time')
        duration = cleaned_data.get('duration')

        if not booking_time_str:
            raise forms.ValidationError("Please select a booking time.")
        if duration is None:
            raise forms.ValidationError("Please select a duration.")

        booking_time = timezone.datetime.combine(timezone.now().date(), booking_time_str)
        end_datetime = booking_time + timezone.timedelta(hours=int(duration))

        cleaned_data['start_time'] = booking_time
        cleaned_data['end_time'] = end_datetime

        return cleaned_data
