from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View

from user import models


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(username=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login.html', {"message": message})


class RegisterView(View):

    def get(self, request):
        if request.method == "GET":
            return render(request, "register.html")

    def post(self, request):
        if request.method == "POST":
            return render(request, "login.html")


class LogoutView(View):

    def get(self, request):
        if request.method == "GET":
            return render(request, "index.html")

# Create your views here.
