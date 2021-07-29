from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


def index(request):
    # return HttpResponse('Hello ')
    return HttpResponseRedirect('polls/')


def favicon(request):
    path = r"my_static/images/bilibili.ico"
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type='image/jpg')
