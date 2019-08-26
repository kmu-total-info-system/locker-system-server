from django.contrib import admin

from .models import *

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    base_model = Block  # Explicitly set here!

    list_display = [field.name for field in Block._meta.fields]
    search_fields = ('type','id','value','state')

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    base_model = Sheet  # Explicitly set here!

    list_display = [field.name for field in Sheet._meta.fields]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    base_model = Transaction  # Explicitly set here!

    list_display = [field.name for field in Transaction._meta.fields]

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    base_model = Time  # Explicitly set here!

    list_display = [field.name for field in Time._meta.fields]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    base_model = Permission  # Explicitly set here!

    list_display = [field.name for field in Permission._meta.fields]
