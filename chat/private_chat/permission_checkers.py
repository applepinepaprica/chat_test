from django.core.exceptions import PermissionDenied


def login_required(func):
    def method(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise PermissionDenied('Not logged in!')
        func(self, info, **kwargs)

    return method
