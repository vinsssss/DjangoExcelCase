from django.db import models

class Excel(models.Model):
    # 文件名
    file_name = models.CharField(max_length=128, null=False, unique=True, verbose_name="文件名")
    # 文件上传时间
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="文件上传时间")
    # 文件上传创建者
    creat_by = models.CharField(max_length=128, null=False, verbose_name="文件上传者")

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = "excel_file"
        verbose_name = "Excel文件"
        verbose_name_plural = verbose_name
        ordering = ["creat_time"]


class Items(models.Model):
    # id = models.Index()
    # 来自文件
    come_from = models.ForeignKey(Excel, on_delete=models.CASCADE, default='')
    # 编码
    code = models.IntegerField(max_length=4, null=False, verbose_name="问题编码")
    # 检查项目名称
    project_name = models.CharField(max_length=256, null=False, verbose_name="检查项目名称")
    # 问题单位
    problem_unit = models.CharField(max_length=256, null=False, verbose_name="问题单位")
    # 问题描述
    project_des = models.TextField(verbose_name="发现问题描述")
    # 整改情况
    rectification_sit = models.TextField(verbose_name="整改情况")
    # 负责科室
    responsible_dep = models.CharField(max_length=256, verbose_name="负责督导整改科室")
    # 原因分析
    cause_analysis = models.TextField(verbose_name="原因分析及影响")
    # 后续措施
    next_step = models.TextField(verbose_name="后续管理措施")
    # 备注
    remark = models.TextField(verbose_name="备注")
    # 数据创建时间
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="数据创建时间")
    # 数据创建者
    creat_by = models.CharField(max_length=128, null=False, verbose_name="数据创建者")

    def __str__(self):
        return self.project_name

    def set_data(self, data):
        try:
            self.code = data[1]
            self.project_name = data[2]
            self.problem_unit = data[3]
            self.project_des = data[4]
            self.rectification_sit = data[5]
            self.responsible_dep = data[6]
            self.cause_analysis = data[7]
            self.next_step = data[8]
            self.remark = data[9]
            return True
        except IndexError:
            return False

    class Meta:
        db_table = "excel_items"
        verbose_name = "Excel数据项"
        verbose_name_plural = verbose_name
        ordering = ["creat_time"]
