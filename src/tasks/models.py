from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Task(models.Model):
    description = models.CharField(max_length=64, blank=False)
    dateLimit = models.DateField(null=True, blank=True)
    concluded = models.BooleanField(blank=True, default=False)
    user = models.ForeignKey(User, on_delete=CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Task: {self.description}"
