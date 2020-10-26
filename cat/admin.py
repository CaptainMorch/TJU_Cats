from django.contrib import admin
from .models import Cat, Entry

# Register your models here.
@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    pass

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass