# Create your views here.
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from urllib import unquote
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import datetime, re
from django import forms
from django.http import HttpResponseRedirect
from mytalk.models import User,Store,Label,Comment,Reply,LabelInline,StoreAdmin

#判断用户名是否格式合法
def is_uid_name_valid(uid):
    pattern = re.compile(r'[A-Za-z](\w|_| )*')
    
    if pattern.match(uid) and len(uid) <= 20:
        return True
    return False
    
#判断邮箱格式是否合法
def is_email_name_valid(email):
    pattern = re.compile(r'\w*@(\w)+.(com|cn|org)')
    
    if pattern.match(email) and len(email) <= 20:
        return True
    return False

#判断密码是否合法
def is_password_valid(password):
    pattern = re.compile(r'\w+')
    
    if pattern.match(password) and len(password) <= 20:
        return True
    return False

#判断某个用户名是否已经存在
def is_uid_exist(uid):
    user = User.objects.filter(id = uid)
    if len(user) == 1:
        return True  
    return False

#判断用户是否合法,需要先验证uid和upassword是否为空等格式是否正确
def is_user_valid(uid,upassword):
    if is_uid_name_valid(uid) and is_password_valid(upassword) and is_uid_exist(uid):
        user = User.objects.get(id = uid)
        if user.password == upassword:
            return True
    return False

#更新用户id为新的newid,true代表成功,需要验证用户名id的格式是否合法
def update_user_id(uid,newUid):
    try:
        user = User.objects.get(id = uid)
        
        if is_uid_exist(newUid) == False and is_uid_name_valid(newUid):
            user.id = newUid
            user.save()
            print "save id"
            User.objects.filter(id = uid).delete()
            return True
    except:
        print "more than one or does not exit"    
        
    return False

#更新用户uid的邮箱为email,需要验证email的格式是否合法
def update_user_email(uid,email):
    try:
        user = User.objects.get(id = uid)
        if is_email_name_valid(email):
            user.email = email
            user.save()
            print "save email"
            return True               
    except:
        print uid + "more than one or does not exit"
    
    return False

#更新用户uid的密码为新的密码password
def update_user_password(uid, password):
    try:
        user = User.objects.get(id = uid)
        if is_password_valid(password):
            user.password = password
            user.save()
            print "save password"
            return True
    except:
        print uid + "more than one or does not exit"
    return False

#获得用户信息,包括用户邮箱Email
def getUserMessage(uid):
    try:
        user = User.objects.get(id = uid)
        return {'uid':user.id, 'email':user.email}
    except:
        return {'uid':uid, 'email':''}

#获得用户uid的好友列表
def getFriendsList(uid):
    friends = []
    try:
        user = User.objects.get(id = uid)
        friendsList = user.friends.all()
        
        print friendsList
        for i in friendsList:
            friends.append(i.id)
    except:
        print uid + "more than one or does not exit"
    return friends

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
    return render_to_response('mytalk/index.html',{'uid':uid})

'''显示好友列表''' 
def friends(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})

    uid = request.session.get('uid')
    myFriendsObj = getFriendsList(uid)
    
    return render_to_response('mytalk/friends.html',{'uid':uid,'friendsList':myFriendsObj})
        
'''更改用户信息'''
def exchangeUserMessage(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})
    
    uid = request.session.get('uid')
    userMessage = getUserMessage(uid)
    is_update = True
    
    if request.POST.get('username')!=None and request.POST.get('email')!=None:
        #return HttpResponse(request.POST.get('updatePassword') != request.POST.get('password'))
        message = { 'uid':request.POST.get('username'),'email':request.POST.get('email'),'isEmail':' ','isPassword':' ','isUsername':' '}
        if userMessage['email']!= request.POST.get('email') and is_email_name_valid(request.POST.get('email')) == False:
            message['isEmail'] = '邮箱不合法'
            is_update = False
        
        if userMessage['uid']!= request.POST.get('username') and (is_uid_name_valid(request.POST.get('username')) == False or is_uid_exist(request.POST.get('username'))):
            message['isUsername'] = '用户名不合法或用户名已经存在'
            is_update = False
            
        if request.POST.get('password')!=request.POST.get('updatePassword') or is_password_valid(request.POST.get('password')) == False:
            message['isPassword'] = '密码不合法,或前后密码不一致'
            is_update = False
            
        if is_update:
            update_user_email(uid,request.POST.get('email')) 
            update_user_password(uid,  request.POST.get('password'))
            if update_user_id(uid, request.POST.get('username')):
                uid =  request.session['uid'] = request.POST.get('username')
        
        return render_to_response('mytalk/exchangeUserMessage.html',{'uid':uid,'message':message})
        
    userMessage = getUserMessage(uid)    
    return render_to_response('mytalk/exchangeUserMessage.html',{'uid':uid,'message':userMessage})

def signIn(request):
    return render_to_response('mytalk/signIn.html',{})

