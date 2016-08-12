from django.contrib import admin

from .models import (
    HatUser,
    Hat,
)

admin.site.register(HatUser)
admin.site.register(Hat)
