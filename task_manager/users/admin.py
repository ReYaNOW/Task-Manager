from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'date_joined',
    )
    list_filter = (('date_joined', DateFieldListFilter),)
    search_fields = ['username']
