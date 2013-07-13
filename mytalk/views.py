# Create your views here.
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from urllib import unquote
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import datetime
from django import forms
from django.http import HttpResponseRedirect

def index(request):
    #return HttpResponse('hello')
    return render_to_response('index.html',{})