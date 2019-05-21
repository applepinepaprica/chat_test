from django.db import models
from django.contrib.auth.models import User


class Dialogue(models.Model):
    user1 = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='+')
    user2 = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='+')


class Message(models.Model):
    sender = models.ForeignKey(User, null=False, on_delete=models.PROTECT, related_name='+')
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    dialogue = models.ForeignKey(Dialogue, null=False, on_delete=models.PROTECT, related_name='+')
