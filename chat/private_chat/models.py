from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='+')
    receiver = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='+')
    text = models.TextField()
