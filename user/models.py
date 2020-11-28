from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="用户创建时间")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "website_user"
        verbose_name = "普通用户"
        verbose_name_plural = verbose_name  # 在后台管理时显示表名为"普通用户"
        ordering = ["creat_time"]
