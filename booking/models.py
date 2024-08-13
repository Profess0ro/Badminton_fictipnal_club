from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from enum import Enum
# from datetime import time, timedelta

class CourtType(Enum):
    GRASS = 'GR'
    GRAVEL = 'GV'

class Court(models.Model):
    TYPE_CHOICES = [(tag.name, tag.value) for tag in CourtType]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if not self.start_time or not self.end_time:
            raise ValidationError("Both start time and end time must be provided.")

        now = timezone.now()
        max_advance_booking = timezone.timedelta(days=30)
        min_booking_time = timezone.time(8, 0)
        max_booking_time = timezone.time(18, 0)

        if self.start_time > now + max_advance_booking:
            raise ValidationError("Bookings can only be made up to one month in advance.")

        if not (min_booking_time <= self.start_time.time() <= max_booking_time):
            raise ValidationError("Bookings can only start between 08:00 and 18:00.")

        if not (min_booking_time <= self.end_time.time() <= max_booking_time):
            raise ValidationError("Bookings can only end between 08:00 and 18:00.")

        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(start_time__lt=models.F('end_time'))
                ),
                name='valid_time_range',
            )
        ]