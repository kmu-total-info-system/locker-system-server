from django.contrib import admin

from .models import *

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    base_model = AuthUser  # Explicitly set here!

    list_display = [field.name for field in AuthUser._meta.fields]
    list_filter = (('is_active', admin.BooleanFieldListFilter),
                   ('is_admin', admin.BooleanFieldListFilter),)

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = AuthUser.objects.filter(pk=obj.pk)
            if obj.is_admin:
                if len(orig_obj) > 0:
                    if obj.password != orig_obj[0].password:
                        obj.set_password(obj.password)
                else:
                    obj.set_password(obj.password)

        else:
            if obj.is_admin:
                obj.set_password(obj.password)
        obj.save()


