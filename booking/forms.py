from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    DURATION_CHOICES = [
        (1, '1 hour'),
        (2, '2 hours'),
    ]
    
    duration = forms.ChoiceField(choices=DURATION_CHOICES, label="Duration", initial=1)

    class Meta:
        model = Booking
        fields = ['court', 'duration']
        widgets = {
            'start_time': forms.HiddenInput(),  # Hide these fields in the form
            'end_time': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_time_str = self.data.get('booking-time')
        duration = int(cleaned_data.get('duration'))

        if not booking_time_str:
            raise forms.ValidationError("Please select a booking time.")

        booking_time = timezone.datetime.strptime(booking_time_str, "%H:%M").time()
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(timezone.now().date(), booking_time)
        )
        end_datetime = start_datetime + timezone.timedelta(hours=duration)

        cleaned_data['start_time'] = start_datetime
        cleaned_data['end_time'] = end_datetime

        return cleaned_data