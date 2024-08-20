from django.db import models

class Rules(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"About Us - {self.id}"