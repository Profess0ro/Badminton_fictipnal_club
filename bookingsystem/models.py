from django.db import models
from datetime import timedelta

class CourtType(models.Model):
    COURT_TYPES = (
        ('GR', 'Grass'),
        ('GV', 'Gravel'),
    )
    type = models.CharField(max_length=2, choices=COURT_TYPES)

    def __str__(self):
        return self.get_type_display()

class Booking(models.Model):
    court_type = models.ForeignKey(CourtType, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='09:00')
    time_slot = models.TimeField(default='08:00')  
    duration = models.DurationField(default=timedelta(minutes=60))

    def __str__(self):
        return f"{self.court_type} - {self.booking_date}"
