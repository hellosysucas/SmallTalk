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
from mytalk.models import User,Store,Label,Comment,Reply,LabelInline,StoreAdmin

#判断用户名是否格式合法
def is_uid_name_valid(uid):
    return True
    
#判断邮箱格式是否合法
def is_email_name_valid(email):
    return True

#更新用户id为新的newid,true代表成功,需要验证用户名id的格式是否合法
def update_user_id(uid,newUid):
    return True

#更新用户uid的邮箱为email,需要验证email的格式是否合法
def update_user_email(uid,email):
    return True

#更新用户uid的密码为新的密码password
def update_user_password(uid,password):
    return True

#判断某个用户名是否已经存在
def is_uid_exist(uid):
    return False

#判断用户是否合法,需要先验证uid和upassword是否为空等格式是否正确
def is_user_valid(uid,upassword):
    return True

#获得用户信息,包括用户邮箱Email
def getUserMessage(uid):
    message = {'uid':uid,'email':'123@qq.com'}
    return message

#获得用户uid的好友列表
def getFriendsList(uid):
    myFriendsObj= ['aa','bb','cc','dd']
    return myFriendsObj

'''主页，登录时设置session为用户 uid,对应于数据库中的id'''
def index(request):
    uid = ''
    if request.POST.get('ope')!= None and request.session.get('uid')!=None:
        del request.session['uid']
    elif request.session.get('uid') == None and request.POST.get('username')!= None :
        uid = request.POST.get('username')
        upassword = request.POST.get('password')
        if is_user_valid(uid,upassword):
            request.session['uid'] = uid
        else:
            uid = ''
    elif request.session.get('uid') != None:
        uid = request.session.get('uid')
    return render_to_response('index.html',{'uid':uid})

'''显示好友列表''' 
def friends(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('index.html',{'uid':uid})

    uid = request.session.get('uid')
    myFriendsObj = getFriendsList(uid)
    
    return render_to_response('friends.html',{'uid':uid,'friendsList':myFriendsObj})
    
'''更改用户信息'''
def exchangeUserMessage(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('index.html',{'uid':uid})
    
    uid = request.session.get('uid')
    userMessage = getUserMessage(uid)
        
    if request.POST.get('username')!=None and request.POST.get('email')!=None:
        #return HttpResponse(request.POST.get('updatePassword') != request.POST.get('password'))
        message = { 'uid':request.POST.get('username'),'email':request.POST.get('email'),'isEmail':' ','isPassword':' ','isUsername':' '}
        if userMessage['email']!= request.POST.get('email'):
            if is_email_name_valid(request.POST.get('email')) == False:
                message['isEmail'] = '邮箱不合法'
            elif update_user_email(uid,request.POST.get('email')) == False:
                message['isEmail'] = '邮箱不合法'
  
        if userMessage['uid']!= request.POST.get('username'):
            if is_uid_name_valid(request.POST.get('username')) == False:
                message['isUsername'] = '用户名不合法'
            elif update_user_id(uid,request.POST.get('username')) == False:
                message['isUsername'] = '用户名不合法'
            else:
                request.session['uid'] = request.POST.get('username')
                uid = request.POST.get('username')
                
        if request.POST.get('password')!=request.POST.get('updatePassword'):
            message['isPassword'] = '密码不合法,或前后密码不一致'
        return render_to_response('exchangeUserMessage.html',{'uid':uid,'message':message})
        
    userMessage = getUserMessage(uid)    
    return render_to_response('exchangeUserMessage.html',{'uid':uid,'message':userMessage})

