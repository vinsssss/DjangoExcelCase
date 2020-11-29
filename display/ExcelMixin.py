import os
import xlrd


class ExcelMixin:

    def __init__(self, path):
        self.workbook = xlrd.open_workbook(path)

    def read_data(self):
        sheet = self.workbook.sheet_by_index(0)
        for row in range(2, sheet.nrows):
            yield sheet.row_values(row)


if __name__ == '__main__':
    file_path = os.path.dirname(os.path.dirname(__file__)) + '/static/excels/' + '(8)财务资产问题管理信息系统.xlsx'
    deal = ExcelMixin(file_path)
    res_list = deal.read_data()
    for item in res_list:
        print(item)
