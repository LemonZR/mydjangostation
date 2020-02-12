from django.shortcuts import render, render_to_response, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Question, Choice


# Create your views here.
def login(request):
    if request.session.get('user', None) == 'zr' and request.session.get('passwd', None) == '123':
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'login.html')


def checklogin(request):
    user = request.POST.get('user', None)
    passwd = request.POST.get('passwd', None)
    print('POST user:%s' % user)
    if user == 'zr' and passwd == '123':
        request.session.set_expiry(30)
        request.session['user'] = user
        request.session['passwd'] = passwd
        return HttpResponseRedirect(reverse('index'))
        #return render(request, 'index.html', {'name': request.session.get('user')})
    else:
        return HttpResponseRedirect(reverse('login'))


# return HttpResponseRedirect(reverse('login'))


def hello(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/hello/')
    return render(request, "hello.html", {'name': request.session.get('user', None)})


def touch(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/polls/touch/')
    return render(request, 'touch.html')


def index(request):
    # 最近的5个question
    user = request.session.get('user', None)
    request.session.set_expiry(30)
    if user:
        print('indexssssssssssssssssssss' + user)
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return render(request, "index.html", {'latest_question_list': latest_question_list, 'questions': output})
    else:
        return HttpResponseRedirect(reverse('login'))


def vote(request, question_id):
    if request.method == 'POST':
        print("I'm question_id %s" % question_id)

        choice_id = request.POST.get('choice_id', None)

        print("I'm choice_id %s" % choice_id)
        try:
            choice = Choice.objects.get(id=choice_id, question_id=question_id)
            print(choice)
            choice.votes = choice.votes + 1
            choice.save()
        except Exception as e:
            print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return HttpResponse("You're voting on question %s." % question_id)


def detail(request, question_id):
    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question_id=question_id)
    return render_to_response("detail.html", {'question': question, 'choices': choices})


def results(request, question_id):
    return HttpResponse("You're looking at the results of the question %s." % question_id)

