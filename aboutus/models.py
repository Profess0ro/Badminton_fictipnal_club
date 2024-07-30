from django.db import models

class AboutUs(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"About Us - {self.id}"