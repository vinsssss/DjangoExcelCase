import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from display import models
from display.models import Excel, Items
from display.excelDealUtil import ExcelDealUtil

class IndexView(View):

    def get(self, request):
        if request.session.get('is_login', None):
            return render(request, 'index.html', {'is_login': request.session['is_login'],
                                                  'user_name': request.session['user_name']})
        else:
            return redirect('/login/')


def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get('file', None)
        try:
            if file:
                excel_name = file.name
                if excel_name.endswith('.xlsx') or excel_name.endswith('xls'):
                    exist_excel = models.Excel.objects.filter(file_name=excel_name)
                    if exist_excel:
                        # 防止命名重复
                        max_id = models.Excel.objects.all().order_by('-id')[0].id + 1
                        excel_name = '(' + str(max_id) + ')' + excel_name

                    file_path = os.path.dirname(os.path.dirname(__file__)) + '/static/excels/' + excel_name
                    print(file_path)
                    with open(file_path, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                    f.close()

                    # excel写入数据库中
                    my_excel = Excel()
                    my_excel.file_name = excel_name
                    my_excel.creat_by = request.session['user_name']
                    my_excel.save()

                    my_excel_util = ExcelDealUtil(file_path)
                    data = my_excel_util.read_data()
                    for data_item in data:
                        my_item = Items()
                        if my_item.set_data(data_item):
                            my_item.creat_by = request.session['user_name']
                            my_item.come_from = my_excel
                            my_item.save()
                        else:
                            raise Exception('添加数据失败！')
                    message = '[OK]上传成功!'
                    return render(request, 'index.html', locals())
                else:
                    raise Exception('文件类型不符！')
            else:
                raise Exception('文件获取失败！')
        except Exception as e:
            message = '[ERROR]上传失败!'
            print(e)
            return render(request, 'index.html', locals())
