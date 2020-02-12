from django.shortcuts import render, render_to_response, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.


def index(request):

    return HttpResponse('Hello ')


