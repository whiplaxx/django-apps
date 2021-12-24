from django.db import models

class Task(models.Model):
    description = models.CharField(max_length=64, blank=False)
    dateLimit = models.DateField(null=True, blank=True)
    concluded = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"Task: {self.description}"

