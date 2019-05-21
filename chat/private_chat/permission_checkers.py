from django.core.exceptions import PermissionDenied
from .models import Dialogue
from graphql_relay.node.node import from_global_id


def login_required(func):
    def method(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise PermissionDenied('Not logged in!')
        func(self, info, **kwargs)

    return method


def is_owner(func):
    def method(self, info, **kwargs):
        user = info.context.user
        dialogue = Dialogue.objects.get(id=from_global_id(kwargs.get('dialogue_id'))[1])
        if dialogue.user1 != user and dialogue.user2 != user:
            raise PermissionDenied('Forbidden!')
        func(self, info, **kwargs)

    return method
