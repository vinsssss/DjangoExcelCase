from django.db import models


class Items(models.Model):
    # id = models.Index()
    code = models.CharField(max_length=4, null=False)
    # 检查项目名称
    project_name = models.CharField(max_length=256, null=False)
    # 问题单位
    problem_unit = models.CharField(max_length=256, null=False)
    # 问题描述
    project_des = models.TextField()
    # 整改情况
    rectification_sit = models.TextField()
    # 负责科室
    responsible_dep = models.CharField(max_length=256)
    # 原因分析
    cause_analysis = models.TextField()
    # 后续措施
    next_step = models.TextField()
    # 备注
    remark = models.TextField()
    # 数据创建时间
    creat_time = models.DateTimeField(auto_now_add=True)
    # 数据最后修改时间
    last_modify_time = models.DateTimeField(auto_now_add=True)
    # 数据创建者
    creat_by = models.CharField(max_length=128, null=False)
    # 数据最后修改者
    last_modify_by = models.CharField(max_length=128, null=False)


class Excel(models.Model):
    # 文件名
    file_name = models.CharField(max_length=128, null=False, unique=True)
    # 文件上传时间
    creat_time = models.DateTimeField(auto_now_add=True)
    # 文件上传创建者
    creat_by = models.CharField(max_length=128, null=False)
