from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class MyUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'is_admin']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']

    readonly_fields = ['last_login']
    ordering = ['id']

    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, MyUserAdmin)


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ['advisor_name', 'advisor_photo_url']
    search_fields = ['advisor_name']
    list_filter = ['advisor_name']

admin.site.register(Advisor,AdvisorAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'advisor']
    search_fields = ['user', 'advisor']
    list_filter = ['user', 'advisor']

admin.site.register(Booking,BookingAdmin)

