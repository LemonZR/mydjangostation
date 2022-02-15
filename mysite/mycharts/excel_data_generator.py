import pprint

import openpyxl
import time


def getData(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\核对清单\aaa_mk日模型核对情况-整体.xlsx', sheet_name='差异清单指标级'):
# def getData(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\核对清单\bbb_mk月模型核对情况-整体.xlsx', sheet_name='mk月模型差异清单指标级'):
    data_dict = {}
    wb = openpyxl.load_workbook(file_name)
    sheet = wb[sheet_name]
    data = list(sheet.rows)[1:]  # 1.首行为标题内容 2.需要用循环判断为空则跳过

    rows_value = list(x for x in list(map(lambda x: list(map(lambda y: y.value, x)), [x for x in data])))
    for line in rows_value:
        """['mk.tm_ac_owefee_down_d', '20210701', '231104', '0', 'pay_fee', '6010030.00', '0.00', '231104', 
        '6010030.00', '20210825', '1.000000', '1.000000'] """
        table_name = line[0]

        if not table_name:
            # 为空则跳过
            continue

        day = time.strftime('%Y-%m-%d', time.strptime(str(line[1]), '%Y%m%d'))
        # day = time.strftime('%Y-%m', time.strptime(str(line[1]), '%Y%m'))
        prov_total = float(line[2])
        jt_total = line[3]
        column_name = line[4]
        column_prov_value = line[5]
        column_jt_value = line[6]
        total_count_diff = float(line[7])
        column_count_diff = line[8]
        update_date = line[9]
        total_diff_rate = float(line[10])
        column_diff_rate = float(line[11])

        data_dict.setdefault(table_name, {}).setdefault('total_diff_rate', {}).setdefault(day, total_diff_rate)
        data_dict.setdefault(table_name, {}).setdefault('column_diff_rate', {}).setdefault(column_name, {}).setdefault(
            day, column_diff_rate)
    # excel_data = list(zip(data_dict.keys(), data_dict.values()))

    return data_dict


def get_dep(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\数据核对参考文档\省内所有表和直接依赖表关系.xlsx', sheet_name='Sheet1'):
    data_dict = {}
    wb = openpyxl.load_workbook(file_name)
    sheet = wb[sheet_name]
    data = list(sheet.rows)[1:]  # 1.首行为标题内容 2.需要用循环判断为空则跳过
    table_dict = {}
    rows_value = list(x for x in list(map(lambda x: list(map(lambda y: y.value, x)), [x for x in data])))
    for line in rows_value:
        """['mk.tm_ac_owefee_down_d', '20210701', '231104', '0', 'pay_fee', '6010030.00', '0.00', '231104', 
        '6010030.00', '20210825', '1.000000', '1.000000'] """
        table_name = line[1]

        if not table_name:
            # 为空则跳过
            continue
        dep_name = line[2]
        table_dict.setdefault(table_name, []).append(dep_name)

    return table_dict


if __name__ == '__main__':
    dt = getData()

    # pprint.pprint(dt)
