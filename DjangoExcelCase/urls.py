"""DjangoExcelCase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

import display
from DjangoExcelCase import settings
from display.views import IndexView
from user.views import LoginView, RegisterView, LogoutView
from django.views.static import serve

urlpatterns = [
    path('', admin.site.urls),
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('index/', IndexView.as_view(), name='index'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('upload/', display.views.upload_file),
    # 文件下载
    url(r'^excels/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
