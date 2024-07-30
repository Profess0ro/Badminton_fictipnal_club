from django.db import models

class Aboutus(models.Model):
    content = models.TextField()
    
    def __str__(self):
        return self.title