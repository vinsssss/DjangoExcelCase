from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View

from user import models
from user.form import UserForm, RegisterForm

import hashlib


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    # update方法只接收bytes类型
    h.update(s.encode())
    return h.hexdigest()


class LoginView(View):

    def get(self, request):
        if request.session.get('is_login', None):
            # print("###################")
            # print(request.session['user_name'])
            # print(request.session['is_login'])
            return redirect('/index/')
        else:
            login_form = UserForm()
            # print(locals())
            return render(request, 'login.html', locals())

    def post(self, request):
        if request.session.get('is_login', None):
            return redirect('/index/')
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.password == hash_code(password):
                    # 是否登录标志
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())


class LogoutView(View):

    def get(self, request):
        if not request.session.get('is_login', None):
            # 如果本来就未登录，也就没有登出一说
            return redirect("/login")
        else:
            request.session.flush()
            return redirect("/login")


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        message = "[ERROR]请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
        else:
            return render(request, 'register.html', locals())
