from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from enum import Enum

class CourtType(Enum):
    GRASS = 'GR'
    GRAVEL = 'GV'

class Court(models.Model):
    TYPE_CHOICES = [(tag.name, tag.value) for tag in CourtType]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)

class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        now = timezone.now().time()  # Correctly obtaining the current time
        max_advance_booking = timezone.timedelta(hours=24*30)  # One month in advance
        min_booking_time = timezone.time(8, 0)
        max_booking_time = timezone.time(18, 0)

        if self.start_time < now + max_advance_booking:
            raise ValidationError("Bookings can only be made up to one month in advance.")
        elif self.start_time.time() < min_booking_time or self.end_time.time() > max_booking_time:
            raise ValidationError("Bookings can only be made between 8:00 and 18:00.")

        # Additional checks or logic can be added here as needed

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(start_time__lt=models.F('end_time'))
                    & models.Q(end_time__gt=models.F('start_time'))
                ),
                name='valid_time_range',
            )
        ]
