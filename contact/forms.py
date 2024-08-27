from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ('membership', 'Membership'),
        ('general_question', 'General question'),
        ('booking_question', 'Bookings'),
    ]
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    name = forms.CharField(max_length=100)
    email = forms.CharField(validators=[EmailValidator()])
    message = forms.CharField(widget=forms.Textarea)
    