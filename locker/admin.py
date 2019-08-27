from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from admin_view_permission import admin as view_admin
from openpyxl.writer.excel import save_virtual_workbook

from locker import generator
from .models import *

@admin.register(Block)
class BlockAdmin(view_admin.AdminViewPermissionModelAdmin):
    base_model = Block  # Explicitly set here!

    list_display = [field.name for field in Block._meta.fields]
    search_fields = ('type','id','value','state')

@admin.register(Sheet)
class SheetAdmin(view_admin.AdminViewPermissionModelAdmin):
    base_model = Sheet  # Explicitly set here!

    list_display = [field.name for field in Sheet._meta.fields]

@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin,view_admin.AdminViewPermissionModelAdmin):
    base_model = Transaction  # Explicitly set here!

    list_display = [field.name for field in Transaction._meta.fields]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('export/', self.export),
        ]
        return my_urls + urls

    def export(self, request):
        # self.model.objects.all().update(is_immortal=True)
        transactions = Transaction.objects.all()
        datas = []
        for transaction in transactions:
            datas.append({'name': transaction.user.name, 'user_id': transaction.user.user_id, 'organization': '제 3대 소프트웨어 융합 학생회 리턴', 'locker': transaction.block.value, 'grade': transaction.user.grade})

        wb = generator.generate(datas)
        print(wb)
        self.message_user(request, "done")
        return HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')

    change_list_template = "change_list.html"
@admin.register(Time)
class TimeAdmin(view_admin.AdminViewPermissionModelAdmin):
    base_model = Time  # Explicitly set here!

    list_display = [field.name for field in Time._meta.fields]


@admin.register(Permission)
class PermissionAdmin(view_admin.AdminViewPermissionModelAdmin):
    base_model = Permission  # Explicitly set here!

    list_display = [field.name for field in Permission._meta.fields]
