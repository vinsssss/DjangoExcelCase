from django.contrib import admin
from django.core.paginator import Paginator

from display import models


class ItemInline(admin.TabularInline):
    model = models.Items


class ItemAdmin(admin.ModelAdmin):
    # inlines = [ItemInline]  # Inline
    search_fields = ('code', 'project_name', 'problem_unit', 'responsible_dep', 'creat_by')
    list_display = ('project_name', 'code', 'problem_unit')
    list_per_page = 10
    paginator = Paginator

    def get_queryset(self, request):  # 重写get_queryset
        qs = super(ItemAdmin, self).get_queryset(request)
        if request.user.is_superuser:  # 判断如果是超级管理员返回所有信息
            return qs
        else:
            print(request.user)
            return qs.filter(creat_by=request.user)


class ExcelAdmin(admin.ModelAdmin):
    # inlines = [ItemInline]  # Inline
    search_fields = ('file_name', 'creat_by')
    list_per_page = 10
    paginator = Paginator


admin.site.site_header = '财务资产问题管理系统'  # 设置header
admin.site.site_title = 'FAPMS'

admin.site.register(models.Items, ItemAdmin)
admin.site.register(models.Excel, ExcelAdmin)
