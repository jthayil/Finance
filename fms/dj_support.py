from django.shortcuts import redirect
from django.db import models


def redirect_homepage(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:homepage")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if (
                request.user.profile.role in allowed_roles
                or request.user.is_staff
                or request.user.is_superuser
            ):
                return view_func(request, *args, **kwargs)
            return redirect("accounts:home")

        return wrapper_func

    return decorator


class ActiveManager(models.Manager):
    def get_queryset(self):
        return (
            super(ActiveManager, self)
            .get_queryset()
            .filter(is_Active=True, deleted=False)
        )


class InactiveManager(models.Manager):
    def get_queryset(self):
        return (
            super(InactiveManager, self)
            .get_queryset()
            .filter(is_Active=False, deleted=False)
        )


class ActiveDeleteManager(models.Manager):
    def get_queryset(self):
        return (
            super(ActiveManager, self)
            .get_queryset()
            .filter(is_Active=True, deleted=True)
        )


class InactiveDeleteManager(models.Manager):
    def get_queryset(self):
        return (
            super(InactiveManager, self)
            .get_queryset()
            .filter(is_Active=False, deleted=True)
        )


# eof
