from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BASEUser
from . import models


@admin.register(models.User)
class UserAdmin(BASEUser):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "first_name", "last_name", "email"),

            },
        ),
    )
