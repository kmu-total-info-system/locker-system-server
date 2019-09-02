from django.contrib import admin, auth
from admin_view_permission import admin as view_admin
from import_export.admin import ImportExportModelAdmin

from .models import *


@admin.register(AuthUser)
class AuthUserAdmin(view_admin.AdminViewPermissionModelAdmin):
    base_model = AuthUser  # Explicitly set here!

    list_display = [field.name for field in AuthUser._meta.fields if field.name not in ['username',
                                                                                        'is_superuser',
                                                                                        'user_permissions',
                                                                                        'password',
                                                                                        'groups',
                                                                                        'is_admin',
                                                                                        'last_login', ]]
    list_filter = (('is_active', admin.BooleanFieldListFilter),
                   ('is_admin', admin.BooleanFieldListFilter),
                   ('time', admin.ChoicesFieldListFilter)
                   )
    search_fields = ('user_id', 'name', 'college', 'school', 'grade')

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
                'password',
                'groups',
                'is_admin',
                'last_login',
            }

        # Prevent non-superusers from editing their own permissions
        if (
                not is_superuser
                and obj is not None
                and obj == request.user
        ):
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
                'password',
                'groups',
                'is_admin',
                'last_login',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
                del form.base_fields[f]

        return form

