from django.db import models
from django.contrib.auth.models import User


class CourtType(models.Model):
    COURT_TYPES = (
        ('GR', 'Grass'),
        ('GV', 'Gravel'),
    )
    type = models.CharField(max_length=2, choices=COURT_TYPES, default='GR')

    def __str__(self):
        return self.get_type_display()


class StartTimes(models.Model):
    start_time = models.TimeField()

    def __str__(self):
        return self.start_time.strftime('%H:%M')


class EndTimes(models.Model):
    end_time = models.TimeField()

    def __str__(self):
        return self.end_time.strftime('%H:%M')


class Booking(models.Model):
    court_type = models.ForeignKey(CourtType, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.ForeignKey(
        StartTimes, on_delete=models.CASCADE, null=True)
    end_time = models.ForeignKey(
        EndTimes, on_delete=models.CASCADE, null=True)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.court_type} - {self.date} from "
            f"{self.start_time} to {self.end_time}"
        )
