from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from django.contrib.auth.models import User
# Register your models here.
class userAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','id')

admin.site.unregister(User)
admin.site.register(User, userAdmin)
admin.site.register(models.person)