from django.shortcuts import render, redirect, reverse, get_object_or_404
# render_to_response（）已弃用，取而代之的是render（）
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Question, Choice
from django.views.decorators.csrf import csrf_exempt
from django.views import View


# 与 from django.views.generic.base import View 同一个View

# Create your views here.


class Login(View):
    def get(self, request):
        user = request.POST.get('user', None)
        if user:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'login.html')

    def post(self, request):
        user_name = request.POST.get('user', None)
        passwd = request.POST.get('passwd', None)
        try:
            user = User.objects.get(name=user_name)
            u_passwd = user.passwd
        except Exception as e:
            user = None
            u_passwd = None
        print('POST user:%s' % user)

        if user is not None and passwd == u_passwd:
            request.session.set_expiry(300)
            request.session['user'] = user
            request.session['passwd'] = passwd
            return HttpResponseRedirect(reverse('index'))
            # return render(request, 'index.html', {'name': request.session.get('user')})
        else:
            return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def logout(request):
    request.session.set_expiry(0)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def hello(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/hello/')
    return render(request, "hello.html", {'name': request.session.get('user', None)})


@csrf_exempt
def touch(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/touch/')
    return render(request, 'touch.html')


@csrf_exempt
def index(request):
    # 最近的5个question
    user = request.session.get('user', None)

    if user:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return render(request, "index.html",
                      {'latest_question_list': latest_question_list, 'questions': output, 'name': user})
    else:
        return HttpResponseRedirect(reverse('login'))


# @csrf_exempt
# 用detail 类视图取代
# def vote(request, question_id):
#
#     isSuccessful = False
#     if request.method == 'POST':
#         print("I'm question_id %s" % question_id)
#
#         choice_id = request.POST.get('choice_id', None)
#         question = get_object_or_404(Question, pk=question_id)
#         choices = Choice.objects.filter(question_id=question_id)
#         print("I'm choice_id %s" % choice_id)
#         try:
#             choice = Choice.objects.get(id=choice_id, question_id=question_id)
#             print(choice)
#             choice.votes = choice.votes + 1
#             choice.save()
#             isSuccessful = True
#         except Exception as e:
#             print(e)
#     kw = {'question': question, 'choices': choices, 'voted_choice_id': choice_id, 'isVoted': True,
#           'isSuccessful': isSuccessful}
#
#     return render(request, 'detail.html', kw)
#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Detail(View):
    def is_login(self, request):
        user = request.session.get('user', None)
        return bool(user)

    def get(self, request, question_id):
        has_login = self.is_login(request)
        # question = Question.objects.get(pk=question_id)
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        return render(request, "detail.html",
                      {'has_login': has_login, 'next': next, 'question': question, 'choices': choices})

    def post(self, request, question_id):
        has_login = self.is_login(request)
        if not has_login:
            return HttpResponseRedirect(reverse('login'))
        else:
            user = request.session.get('user')
        isSuccessful = False
        choice_id = request.POST.get('choice_id', None)
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question_id=question_id)
        print("I'm choice_id %s" % choice_id)

        # 投票的id，session中使用，判断是否重复投票
        voted_id = '%s-%s' % (question_id, user)
        voted_choice_id = request.session.get('voted_choice_id', choice_id)
        # 页面需要的信息
        kw = {'question': question, 'choices': choices, 'voted_choice_id': voted_choice_id, 'isVoted': True,
              'isSuccessful': isSuccessful, 'Duplicate_Submission': False}

        if not request.session.get(voted_id, False):
            request.session['voted_choice_id'] = voted_choice_id
        else:
            kw.update({'Duplicate_Submission': True})
            return render(request, 'detail.html', kw)
        try:
            choice = Choice.objects.get(id=choice_id, question_id=question_id)
            print(choice)
            choice.votes = choice.votes + 1
            choice.save()
            isSuccessful = True
        except Exception as e:
            print(e)
        kw.update({'isSuccessful': isSuccessful})

        request.session[voted_id] = isSuccessful
        return render(request, 'detail.html', kw)


import json


def user_info(request):
    # print ".........",request.META
    ip_addr = request.META['REMOTE_ADDR']
    user_ua = request.META['HTTP_USER_AGENT']

    result = {"STATUS": "success",
              "INFO": "User info",
              "IP": ip_addr,
              "UA": user_ua}

    return HttpResponse(json.dumps(result), content_type="application/json")


def results(request, question_id):
    return HttpResponse("You're looking at the results of the question %s." % question_id)
