from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class IndexView(View):

    def get(self, request):
        if request.session.get('is_login', None):
            return render(request, 'index.html', {'is_login': request.session['is_login'],
                                                  'user_name': request.session['user_name']})
        else:
            # message = '请登录！'
            return redirect('/login/')
            # return render(request, "login.html")