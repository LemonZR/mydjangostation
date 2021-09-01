from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.


def index(request):
    # return HttpResponse('Hello ')
    return HttpResponseRedirect('mycharts/')


def favicon(request):
    path = r"my_static/images/bilibili.ico"
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type='image/jpg')


def error_404(request, exception):
    return render(request,'error404.html')


def error_500(request):
    return render(request,'error404.html')
