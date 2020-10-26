from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Campus, Location

admin.site.register(User, UserAdmin)

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass