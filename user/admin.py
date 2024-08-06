from django.contrib import admin
from django.contrib.auth.models import User
from .models import Additional_Fiels
from django.contrib.auth.admin import UserAdmin

class AccountInline(admin.StackedInline):
    model= Additional_Fiels
    can_delete =False
    verbose_name_plural = 'UsersProfile'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

admin.site.register(Additional_Fiels)