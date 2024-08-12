from django import forms
from .models import Court, Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['court', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['court'].queryset = Court.objects.all()
        self.fields['start_time'].widget.attrs.update({'type': 'datetime-local'})
        self.fields['end_time'].widget.attrs.update({'type': 'datetime-local'})