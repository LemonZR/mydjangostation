import os
import sys
import time

from django.shortcuts import render, redirect, reverse, get_object_or_404
# render_to_response（）已弃用，取而代之的是render（）
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Question, Choice
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from pyecharts import charts

from .authenticated import is_authenticated, class_method_authenticated

import json


# 与 from django.views.generic.base import View 同一个View

# Create your views here.


class Login(View):
    def get(self, request):
        user = request.session.get('user', None)
        referer = request.session.get('HTTP_REFERER', '')

        if user:
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/login.html')

    def post(self, request):
        user_name = request.POST.get('user', None)
        passwd = request.POST.get('passwd', None)
        referer = request.session.get('HTTP_REFERER', '')
        try:
            user = User.objects.get(name=user_name)
            u_passwd = user.passwd
        except Exception as e:
            user = None
            u_passwd = None
        print('POST user:%s' % user)

        if user is not None and passwd == u_passwd:
            request.session.set_expiry(600)
            request.session['user'] = user_name
            request.session['passwd'] = passwd
            if referer:
                request.session['HTTP_REFERER'] = ''
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect(reverse('polls:index'))
            # return render(request, 'index.html', {'name': request.session.get('user')})
        else:
            return HttpResponseRedirect(reverse('polls:login'))


@csrf_exempt
def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('polls:login'))


@csrf_exempt
@is_authenticated
def hello(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/hello/')
    return render(request, "polls/hello.html", {'name': request.session.get('user', None)})


@csrf_exempt
def touch(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/touch/')
    # 删除管理员
    # from django.contrib.auth.models import User
    # user = User.objects.get_by_natural_key('zr')
    # user.delete()
    #
    return render(request, 'polls/touch.html')


@csrf_exempt
def index(request):
    # 最近的5个question
    user = request.session.get('user', None)

    if user:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return render(request, "polls/index.html",
                      {'latest_question_list': latest_question_list, 'questions': output, 'name': user})
    else:
        return HttpResponseRedirect(reverse('polls:login'))


class Detail(View):
    @class_method_authenticated
    def get(self, request, question_id):
        user = request.session.get('user', None)
        has_login = bool(user)
        # question = Question.objects.get(pk=question_id)
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        return render(request, "polls/detail.html",
                      {'has_login': has_login, 'next': next, 'question': question, 'choices': choices, 'name': user})

    @class_method_authenticated
    def post(self, request, question_id):
        user = request.session.get('user', None)
        has_login = bool(user)
        if not has_login:
            return HttpResponseRedirect(reverse('polls:login'))

        isSuccessful = False
        choice_id = request.POST.get('choice_id', None)
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        print("I'm choice_id %s" % choice_id)

        # 投票的id，session中使用，判断是否重复投票
        voted_id = '%s-%s' % (question_id, user)
        voted_choice = request.session.get(voted_id, choice_id)
        print(voted_choice + 'asdasdasd')
        # 页面需要的信息
        kw = {'question': question, 'choices': choices, 'voted_choice': voted_choice, 'isVoted': True,
              'isSuccessful': isSuccessful, 'Duplicate_Submission': False, 'user': user}

        if not request.session.get(voted_id, None):
            request.session[voted_id] = voted_choice
        else:
            kw.update({'Duplicate_Submission': True})
            return render(request, 'polls/detail.html', kw)
        try:
            choice = Choice.objects.get(id=choice_id, question_id=question_id)
            print(choice)
            choice.votes = choice.votes + 1
            choice.save()
            isSuccessful = True
        except Exception as e:
            print(e)
        kw.update({'isSuccessful': isSuccessful})

        return render(request, 'polls/detail.html', kw)


@is_authenticated
def user_info(request):
    # print ".........",request.META
    ip_addr = request.META['REMOTE_ADDR']
    user_ua = request.META['HTTP_USER_AGENT']

    result = {"STATUS": "success",
              "INFO": "User info",
              "IP": ip_addr,
              "UA": user_ua}
    value = request.META.items()
    k = request.META.keys()
    print(k)

    return HttpResponse(json.dumps(result), content_type="application/json")


def results(request, question_id):
    return HttpResponse("You're looking at the results of the question %s." % question_id)


class Register(View):

    def get(self, request):

        return render(request, 'polls/register.html')

    def post(self, request):
        user_name = request.POST.get('user_name')
        passwd = request.POST.get('passwd')

        duplicate_user_name = bool(User.objects.filter(name=user_name))
        if len(passwd) < 3 or len(passwd) > 16:
            just_failed = True
        else:
            just_failed = False

        failed = duplicate_user_name or just_failed
        if not failed:
            request.session['user'] = user_name
            print(user_name)
            new_user = User(name=user_name, passwd=passwd, age=0)
            new_user.save()
            return HttpResponseRedirect(reverse('polls:login'))
        else:
            return render(request, 'polls/register.html',
                          {'failed': failed, 'duplicate_user_name': duplicate_user_name, 'just_failed': just_failed})


@is_authenticated
def beforeDrawing(request):
    user = request.session.get('user', None)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, "polls/drawing.html",
                  {'latest_question_list': latest_question_list, 'name': user})


class Drawing(View):
    @class_method_authenticated
    def get(self, request, question_id):
        print(request.session.get('HTTP_REFERER'))
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        print(question_id)
        choice_list = []
        for choice in choices:
            choice_list.append((choice.choice_text, choice.votes))

        pie_path = 'polls/render/%s_charts.html' % question_id
        if not os.path.exists(pie_path):
            pie = charts.Pie()
            pie.add(question.question_text, choice_list, )
            pie.render(pie_path)
        else:
            pie_mod_time = os.path.getmtime(pie_path)
            print(pie_mod_time)
            print(time.time())
            print(time.time() - pie_mod_time)
            if time.time() - pie_mod_time >= 60:
                pie = charts.Pie()
                pie.add(question.question_text, choice_list, )
                pie.render(pie_path)

        chart = open(pie_path).read()
        return HttpResponse(chart)





