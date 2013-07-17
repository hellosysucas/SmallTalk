# Create your views here.
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from urllib import unquote
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import hashlib
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

#获得某个人的所有评论过的商店的所有评论
def getUserComments(uid):
    comment1 = ["good","very good","not bad"]
    store1 = {"name":"store1","place":"guang zhou","comment":comment1}
    
    comment2 = ["bad","very bad","so bad"]
    store2 = {"name":"store2","place":"shang hai","comment":comment2}
    talk = [store1,store2]
    return talk
    
#删除用户uid的好友friend
def deleteUserFriend(uid,friend):
    return True
    
#插入新的用户到数据库中，密码已经是加密后的
def insert_new_user(email,uid,password):
    return True

'''数据加密'''
def hashPassword(password):
    mySha1 = hashlib.sha1()
    mySha1.update(password)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest

'''主页，登录时设置session为用户 uid,对应于数据库中的id'''
def index(request):
    uid = ''
    '''
    if request.POST.get('ope')!= None and request.session.get('uid')!=None:
        del request.session['uid']
        is_ok = True
    elif request.session.get('uid') == None and request.POST.get('username')!= None :
        uid = request.POST.get('username')
        upassword = request.POST.get('password')
        if len(uid)>0 and len(upassword)>0:
            if is_user_valid(uid,upassword):
                request.session['uid'] = uid
                is_ok = True
            else:
                uid = ''
    elif request.session.get('uid') != None:
        uid = request.session.get('uid')
        is_ok = True
        
    if is_ok == False:
        return render_to_response('mytalk/index.html',{'uid':uid,"showError":"用户名或密码有误,若未注册，请先注册"})
    '''
    if request.session.get('uid') != None:
        uid = request.session.get('uid')
    return render_to_response('mytalk/index.html',{'uid':uid})

'''退出操作'''
def exitOperation(request):
    if request.session.get('uid') != None:
        request.session['uid'] = ''
        del request.session['uid']
    return HttpResponse("true")

'''用户登录'''
def signIn(request):
    return render_to_response("mytalk/signIn.html")

'''验证用户登录'''
def detectLogin(request):
    uid = request.POST.get("username")
    password = request.POST.get("password")
    is_ok = "false"
    if uid!=None and password!=None:
        password = hashPassword(password)
        if is_user_valid(uid,password):
            is_ok = "true"
            request.session['uid'] = uid
    return HttpResponse(is_ok)

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
        
    if request.POST.get('username')!=None and request.POST.get('email')!=None:
        #return HttpResponse(request.POST.get('updatePassword') != request.POST.get('password'))
        message = { 'uid':request.POST.get('username'),'email':request.POST.get('email'),'isEmail':' ','isPassword':' ','isUsername':' '}
        if userMessage['email']!= request.POST.get('email'):
            if is_email_name_valid(request.POST.get('email')) == False:
                message['isEmail'] = '邮箱不合法'
            elif update_user_email(uid,request.POST.get('email')) == False:
                message['isEmail'] = '邮箱不合法'
            else:
                message['isEmail'] = "修改成功"
  
        if userMessage['uid']!= request.POST.get('username'):
            if is_uid_name_valid(request.POST.get('username')) == False:
                message['isUsername'] = '用户名不合法'
            elif update_user_id(uid,request.POST.get('username')) == False:
                message['isUsername'] = '用户名不合法'
            else:
                message['isUsername'] = "修改成功"
                request.session['uid'] = request.POST.get('username')
                uid = request.POST.get('username')
                
        if request.POST.get('password')!=request.POST.get('updatePassword') or len(request.POST.get('password'))==0 or len(request.POST.get('updatePassword'))==0:
            message['isPassword'] = '密码不合法,或前后密码不一致'
        elif request.POST.get('password')!= None and request.POST.get('updatePassword')!=None:
            password = hashPassword(request.POST.get('password'))
            password = hashPassword(password)
            update_user_password(uid,password)
            message['isPassword'] = "密码修改成功"
        return render_to_response('mytalk/exchangeUserMessage.html',{'uid':uid,'message':message})
        
    userMessage = getUserMessage(uid)    
    return render_to_response('mytalk/exchangeUserMessage.html',{'uid':uid,'message':userMessage})
    
'''显示评论信息，如果为自己的话，将显示自己所有的评论；如果是好友的话，显示好友可见的评论'''
def message(request):
    uid = ''
    if request.session.get('uid') == None or request.POST.get('username') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})
        
    uid = request.session.get('uid')
    friend = request.POST.get('username')
    
    talk = getUserComments(uid)
    return render_to_response('mytalk/message.html',{'uid':uid,'friend':friend,'talk':talk})
    
'''删除用户uid的某个好友,返回的结果为一个true 或者是 false，true代表删除成功'''
def deleteFriend(request):
    uid = ''
    if request.session.get('uid') == None or request.POST.get('username') == None:
        return False
    
    return deleteUserFriend(uid,request.POST.get('username'))
        
'''用户注册'''
def register(request):
    return render_to_response("mytalk/register.html",{'uid':''})
    
'''完成注册过程'''
def doRegister(request):
    #return HttpResponse("hello")
    email = request.POST.get("email")
    uid = request.POST.get("username")
    password = request.POST.get("password")
    
    if is_email_name_valid(email) and is_uid_name_valid(uid) and len(password)>0:
        if  is_uid_exist(uid)==False and insert_new_user(email,uid,hashPassword(password)):
            request.session['uid'] = uid
            return HttpResponse("true")
        else:
            return HttpResponse("用户名已存在")
    else:
        return HttpResponse("false")
        