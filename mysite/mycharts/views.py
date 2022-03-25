import datetime
import os
import sys
import time

from django.shortcuts import render, redirect, reverse, get_object_or_404
# render_to_response（）已弃用，取而代之的是render（）
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TableData, TableDependence
from polls.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from pyecharts import charts
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from .authenticated import is_authenticated, class_method_authenticated
from .excel_data_generator import getData, get_dep
import json

app_dir = os.path.dirname(__file__)


# project_dir =os.path.dirname(BaseDir)


class Login(View):
    """curl localhost:8000/mycharts/login/
        -F user=z -F passwd=123
        -H "X-CSRFtoken:[the value]"
        -b "csrftoken=[the same as above]"
    """

    def get(self, request):
        user = request.session.get('user', None)
        referer = request.session.get('HTTP_REFERER', '')

        if user:
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse('mycharts:index'))
        return render(request, 'mycharts/login.html')

    def post(self, request):
        user_name = request.POST.get('user', None)
        passwd = request.POST.get('passwd', None)
        referer = request.session.get('HTTP_REFERER', '')
        print('login post :' + referer)
        try:
            user = User.objects.get(name=user_name)
            u_passwd = user.passwd
        except Exception as e:
            user = None
            u_passwd = None
        print('POST user:%s' % user)

        if user is not None and passwd == u_passwd:
            request.session.set_expiry(0)  # 关闭浏览器失效
            request.session['user'] = user_name
            request.session['passwd'] = passwd
            if referer:
                request.session['HTTP_REFERER'] = ''
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse('mycharts:index'))
            # return render(request, 'index.html', {'name': request.session.get('user')})
        else:
            return HttpResponseRedirect(reverse('mycharts:login'))


@csrf_exempt
def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('mycharts:login'))


@is_authenticated
# @csrf_exempt
def index(request):
    user = request.session.get('user')
    table_name = TableData.objects.filter(table_id__lte=10, table_id__gte=0).values('table_name')

    return render(request, 'mycharts/index.html', {'tables': table_name, 'name': user})


@is_authenticated
def searchtable(request):
    if request.method == 'GET':
        return HttpResponse('登录成功了，返回吧。这个页面还没做')
    # time.sleep(0.1)  # 测试前端用户感知，测试结束去掉
    json_data = request.body.decode('utf-8')
    info = json.loads(json_data)
    find_str = info.get('find_str', '')
    current_page = info.get('pn', 1)
    # table_names = TableData.objects.filter(table_name__contains=find_str).values('table_name')[:10]
    table_names = TableData.objects.filter(table_name__contains=find_str).order_by('table_id').values('table_name')
    paginator = Paginator(table_names, 10)  # Paginator生成一个对象，然后传入queryset,
    try:  # 以及每页显示的个数，这里每页显示十个
        page_obj = paginator.page(current_page)  # 根据get方法取到的数字显示页数
    except EmptyPage as e:  # 如果get方法获取了一个没有的页数则显示第一页
        page_obj = paginator.page(1)
    except PageNotAnInteger as e:  # 传入一个字符串也显示第一页
        page_obj = paginator.page(1)
    pagerange = paginator.get_elided_page_range(current_page, on_each_side=3, on_ends=2)
    page_obj.my_page_range = pagerange

    return render(request, 'mycharts/searchresult.html', {'tables': table_names, 'page_obj': page_obj})


@is_authenticated
def update_index(request):
    return render(request, 'mycharts/update.html')


@is_authenticated
def update_table_data(request):
    try:
        mk_day_data = getData(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\核对清单\aaa_mk日模型核对情况-整体.xlsx')
        dis_day_data = getData(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\核对清单\ccc_dis日表整体核对情况.xlsx')
        mk_mon_data = getData(file_name=r'D:\bigdata\集中化搬迁\开发区svn文件\集中化数据核对\核对清单\bbb_mk月模型核对情况-整体.xlsx',
                              sheet_name='mk月模型差异清单指标级', date_format='month')
        data = {**mk_day_data, **mk_mon_data, **dis_day_data}
        sixtyDaysAgo = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
        for key, v in data.items():
            table = TableData.objects.get(table_name=key) if TableData.objects.filter(table_name=key) else TableData(
                table_name=key,table_data=dict())
            #删除数据库中需要更新的记录数差异记录
            min_tot_date,max_tot_date = min(v['total_diff_rate'].keys()),max(v['total_diff_rate'].keys())
            day_exists = list(table.table_data.setdefault('total_diff_rate',{}).keys())
            for day in day_exists:
                if min_tot_date <= day <= max_tot_date or day < sixtyDaysAgo:
                    del table.table_data['total_diff_rate'][day]
            # 删除数据库中需要更新的指标差异记录
            for column,info in v['column_diff_rate'].items():
                # 1.删掉数据库中每个指标相应周期的数据（data中的指标最小和最大账期之间的数据,以及小于sixtyDaysAgo的账期数据），然后更新。
                min_diff_date ,max_diff_date = min(info.keys()),max(info.keys())
                day_exists = list(table.table_data.setdefault('column_diff_rate',{}).setdefault(column,{}).keys())
                for day in day_exists:
                    if min_diff_date <= day <= max_diff_date or day < sixtyDaysAgo:
                        del table.table_data['column_diff_rate'][column][day]

            # 更新
            table.table_data['total_diff_rate'].update(v['total_diff_rate'])
            table.table_data['column_diff_rate'].update(v['column_diff_rate'])
            table.save()
        return HttpResponse('Ok')
    except Exception as e:
        print(e)
        return HttpResponse('No')


def do_once(request):
    try:
        data = get_dep()
        for key, v in data.items():
            table = TableDependence.objects.get(table_name=key) if TableDependence.objects.filter(
                table_name=key) else TableDependence(
                table_name=key)

            table.dependence = v
            table.save()
        return HttpResponse('Ok')
    except Exception as e:
        print(e)
        return HttpResponse('No')


@is_authenticated
def drawtable(request):
    json_data = request.body.decode('utf-8')
    info = json.loads(json_data)
    table_name = info.get('table_name', '').strip()

    # line_path = 'mycharts/render/tabledata/charts_%s.html' % table_name.split('.')[1]
    # 部署到apache服务器后需要使用绝对路径
    line_path = os.path.join(app_dir, 'render/tabledata/charts_%s.html' % table_name.split('.')[1])
    if not os.path.exists(line_path) or time.time() - os.path.getmtime(line_path) > 86400:
        table = get_object_or_404(TableData, table_name=table_name)
        line_name = table.table_name
        table_data = table.table_data
        x_data = table_data.get("total_diff_rate").keys()
        y_data = table_data.get("total_diff_rate").values()
        line = (
            charts.Line()
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),

                ),
                title_opts=opts.TitleOpts(title="差异比", subtitle="单位1")
            )
                .add_xaxis(xaxis_data=x_data)
                .add_yaxis(
                series_name=line_name,
                y_axis=y_data,
                symbol="circle",
                itemstyle_opts=opts.ItemStyleOpts(border_color='#fff'),
                markpoint_opts=opts.MarkPointOpts(
                    label_opts=opts.LabelOpts(color='#fff'),
                    data=[opts.MarkPointItem(type_='max', name='最大值'), opts.MarkPointItem(type_='min', name='最小值'),
                          opts.MarkLineItem(type_="average", name="平均值")]

                ),
                markline_opts=opts.MarkLineItem(type_='average'),
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True
            )
        )
        line.render(line_path)

    chart = open(line_path).read()
    return HttpResponse(chart)


@is_authenticated
def drawtable_detail(request):
    #  time.sleep(0.1)  # 测试前端用户感知
    json_data = request.body.decode('utf-8')
    info = json.loads(json_data)
    table_name = info.get('table_name', '').strip()
    JSFUNC = """<span style='color:yellow;font-size:20px'>节点<span>
     <span style='color:red;font-size:30px'>{line}<br>------<span>"""  # { 图表的名字 line } 或者{ @[index] }
    # line_path = 'mycharts/render/tabledata/charts_%s.html' % table_name.split('.')[1]
    # 部署到apache服务器后需要使用绝对路径
    line_path = os.path.join(app_dir, 'render/tabledata/charts_%s.html' % table_name.split('.')[1])
    if not os.path.exists(line_path) or time.time() - os.path.getmtime(line_path) > 60:
        table = get_object_or_404(TableData, table_name=table_name)
        line_name = table.table_name
        table_data = table.table_data
        x_data = table_data.get("total_diff_rate").keys()
        y_data = table_data.get("total_diff_rate").values()
        column_diff_rate = table_data.get("column_diff_rate")

        line = (
            charts.Line(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
                .set_series_opts(label_opts=opts.LabelOpts(formatter=JSFUNC, position='right'))
                .set_global_opts(
                # toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                #     save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True))),
                tooltip_opts=opts.TooltipOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),

                ),
                title_opts=opts.TitleOpts(title="差异比", subtitle="单位1")
            )
                .add_xaxis(xaxis_data=x_data)
                .add_yaxis(
                series_name=line_name,
                y_axis=y_data,
                symbol="circle",
                itemstyle_opts=opts.ItemStyleOpts(border_color='#fff'),
                markpoint_opts=opts.MarkPointOpts(
                    label_opts=opts.LabelOpts(color='red'),
                    data=[opts.MarkPointItem(type_='max', name='最大值'), opts.MarkPointItem(type_='min', name='最小值'),
                          opts.MarkLineItem(type_="average", name="平均值")]

                ),
                markline_opts=opts.MarkLineItem(type_='average'),
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True
            )
        )
        for column, diff_data in column_diff_rate.items():
            tmp = []
            for day in x_data:
                tmp.append(diff_data.get(day, None))
            line.add_yaxis(
                series_name=column,
                y_axis=tmp,
                symbol="circle",
                # itemstyle_opts=opts.ItemStyleOpts(border_color='#fff'),
                # markpoint_opts=opts.MarkPointOpts(
                #     label_opts=opts.LabelOpts(color='#fff'),
                #     data=[opts.MarkPointItem(type_='max', name='最大值'), opts.MarkPointItem(type_='min', name='最小值'),
                #           opts.MarkLineItem(type_="average", name="平均值")]
                #
                # ),

                markline_opts=opts.MarkLineItem(type_='average'),
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                is_connect_nones=True
            )

        line.render(line_path)

    chart = open(line_path).read()
    return HttpResponse(chart)


class RESTfulTest(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')

    def delete(self, request):
        return HttpResponse('delete')

    def put(self, request):
        return HttpResponse('put')

    def zidingyi(self, request):  # 通过修改 View 类的http_method_names 内容可以增加自定义method
        return HttpResponse('zidingyi')
