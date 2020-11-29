import os

from django.contrib import admin
from django.core.paginator import Paginator

from display import models
from display.ExcelMixin import ExcelMixin
from display.models import Items


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
            # print(request.user)
            return qs.filter(creat_by=request.user)

    class CodeFilter(admin.SimpleListFilter):
        title = '问题编码'  # 过滤标题显示为"以 英雄性别"
        parameter_name = 'code'  # 过滤器使用的过滤字段

        def lookups(self, request, model_admin):
            return (
                ('1001', '制度执行'),
                ('1002', '账户管理'),
                ('1003', '资金收支'),
                ('1004', '特殊资金管理'),
                ('1005', '清欠管理'),
                ('1006', '存货管理'),
                ('1099', '其他资金管理问题'),

                ('2001', '工程成本核算（进度、结算等）'),
                ('2002', '资本性支出与收益性支出划分不准确'),
                ('2003', '资产转资（不及时、滞后等）'),
                ('2004', '资产清查（不及时、账实物不相符等）'),
                ('2005', '资产处置（闲置、评估、报废、处置等）'),
                ('2099', '其他资产类问题'),

                ('3001', '增值税抵扣（应抵未抵、不应抵项目进行抵扣）'),
                ('3002', '税费计提不正确'),
                ('3003', '价格执行不正确'),
                ('3004', '发票方面（退回、丢失、开具红字发票等）'),
                ('3099', '其他税价管理问题'),

                ('4001', '成本费用列支（多列、少列、提前、推后等问题）'),
                ('4002', '费用核销问题（跨期、适用标准不当等）'),
                ('4003', '成本费用确认依据不充分'),
                ('4004', '收入确认（多计、少计、提前、推后等问题）'),
                ('4005', '往来核算（挂账和支付往来单位错误、账龄错误、往来清理不及时等）'),
                ('4099', '其他成本费用类'),

                ('5001', '原始凭证、外部单据不合规、自制票据不规范、未取得适当票据'),
                ('5002', '会计核算科目使用不规范'),
                ('5003', '记账凭证摘要、调账依据不规范'),
                ('5004', '记账凭证处理不及时、不准确'),
                ('5005', '会计档案管理不规范'),
                ('5099', '其他会计基础工作问题'),

            )

        def queryset(self, request, queryset):
            '''定义过滤器的过滤动作'''
            if self.value():
                return queryset.filter(code=self.value()).all()
            # elif self.value() == '2005':
            #     return queryset.filter(code='2005').all()

    list_filter = (CodeFilter, )


class ExcelAdmin(admin.ModelAdmin):
    # inlines = [ItemInline]  # Inline
    search_fields = ('file_name', 'creat_by')
    list_per_page = 10
    paginator = Paginator
    list_display = ('file_name', 'file', 'creat_by')

    # list_display = ['file_name', 'file', 'file_link', 'creat_by']
    def get_queryset(self, request):  # 重写get_queryset
        qs = super(ExcelAdmin, self).get_queryset(request)
        if request.user.is_superuser:  # 判断如果是超级管理员返回所有信息
            return qs
        else:
            # print(request.user)
            return qs.filter(creat_by=request.user)

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('file_name', 'file')
        return super(ExcelAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creat_by = request.user.username
        obj.save()

    def change_view(self, request, object_id, extra_context=None):
        self.fields = ('file_name', 'file', 'creat_by')
        self.readonly_fields = ('creat_by',)
        # print(request)
        return super(ExcelAdmin, self).change_view(request, object_id, extra_context=extra_context)

    actions = ['export_as_excel_items']

    def export_as_excel_items(self, request, queryset):
        # meta = self.model._meta
        # file_name = meta.file.name
        for obj in queryset:
            file_name = obj.file.name
            # print(file_name)
            file_path = os.path.dirname(os.path.dirname(__file__)) + '/excels/' + file_name
            my_excel_util = ExcelMixin(file_path)
            data = my_excel_util.read_data()
            for data_item in data:
                my_item = Items()
                if my_item.set_data(data_item):
                    my_item.creat_by = request.user.username
                    my_item.come_from = obj
                    my_item.save()
                else:
                    raise Exception('添加数据失败！')

    export_as_excel_items.short_description = '导入EXCEL数据'


admin.site.site_header = '财务资产问题管理系统'  # 设置header
admin.site.site_title = 'FAPMS'

admin.site.register(models.Items, ItemAdmin)
admin.site.register(models.Excel, ExcelAdmin)
