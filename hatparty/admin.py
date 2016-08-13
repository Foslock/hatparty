from django.contrib import admin

from .models import (
    HatUser,
    Hat,
    Like,
    Slap,
    HatTransfer,
)

admin.site.register(HatUser)
admin.site.register(Like)
admin.site.register(Slap)
admin.site.register(HatTransfer)
admin.site.register(Hat)
