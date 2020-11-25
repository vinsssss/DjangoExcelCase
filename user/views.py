from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View


class LoginView(View):

    def get(self, request):
        if request.method == "GET":
            return render(request, "login.html")

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("pwd")
            print("user:"+username)
            print("pwd:"+password)
            valid_num = request.POST.get("valid_num")
            keep_str = request.session.get("keep_str")
            if keep_str.upper() == valid_num.upper():
                user_obj = auth.authenticate(username=username, password=password)
                print(user_obj.username)


# Create your views here.
