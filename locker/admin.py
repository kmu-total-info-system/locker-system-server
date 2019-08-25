from django.contrib import admin

from .models import *

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    base_model = Block  # Explicitly set here!

    list_display = [field.name for field in Block._meta.fields]

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    base_model = Sheet  # Explicitly set here!

    list_display = [field.name for field in Sheet._meta.fields]
