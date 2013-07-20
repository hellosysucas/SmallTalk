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
#判断某一个商店是否存在，传递过来的是商店名字符串
def is_store_exist(store_name):
	return True
	
#获得用户信息,包括用户邮箱Email
def getUserMessage(uid):
    message = {'uid':uid,'email':'123@qq.com'}
    return message

#获得用户uid的好友列表
def getFriendsList(uid):
    myFriendsObj= ['aa','bb','cc','dd']
    return myFriendsObj

#获得某个人的所有评论过的商店的所有评论
def getUserComments(uid):
    comment1 = ["good","very good","not bad","4"]
    store1 = {"name":"store1","place":"guang zhou","comment":comment1}
    
    comment2 = ["bad","very bad","so bad","4"]
    store2 = {"name":"store2","place":"shang hai","comment":comment2}
    talk = [store1,store2]
    return talk
    
#获得公开的所有商店的所有评论,注意，是公开显示的评论
def getCommonComments():
    comment1 = ["good","very good","not bad","4"]
    store1 = {"name":"store1","place":"guang zhou","comment":comment1}
    
    comment2 = ["bad","very bad","so bad","4"]
    store2 = {"name":"store2","place":"shang hai","comment":comment2}
    
    comment3 = ["bad3","very bad3","so bad3","4"]
    store3 = {"name":"store3","place":"shang hai","comment":comment3}
    talk = [store1,store2,store3]
    return talk    

#插入一条新的评论，comment为评论内容，store_name为商店名，uid为用户，visibility为一个int类型的值，1代表公共可见，0代表好友可见
def insert_new_comment(comment,store_name,uid,visibility):
    return True

#获取热门商店,以及评论
def getHostStore():
    comment1 = ["good","very good","not bad","4"]
    store1 = {"name":"store1","place":"guang zhou","comment":comment1}
    
    comment2 = ["bad","very bad","so bad","4"]
    store2 = {"name":"store2","place":"shang hai","comment":comment2}
    talk = [store1,store2]
    return talk

#获得第page+1个四个商店名，例如第零页的四个商店名，第二页的四个商店名
def getPageStoreList(page):
    storeList = ["store1","store2","store3","store4"]
    return storeList
    
#获得某一个商店的所有评论信息,store 为商店名,最后返回一个只有一个元素的数组,方便函数重用,如果没有这个商店，返回一个空数组
def getTheStoreMessage(store):
    comment1 = ["good","very good","not bad","4"]
    theStore = {"name":store,"place":"guang zhou","comment":comment1}
    
    talk = [theStore]
    return talk
    
#插入新的商店，插入成功返回true
def insert_new_store(store_name,store_place):
    return True
    
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
        return render_to_response('index.html',{'uid':uid,"showError":"用户名或密码有误,若未注册，请先注册"})
    '''
    hostStore = getHostStore()
    if request.session.get('uid') != None:
        uid = request.session.get('uid')
        friendsList = getFriendsList(uid)
        return render_to_response('mytalk/index.html',{'uid':uid,'friendsList':friendsList,'hostStore':hostStore})
    return render_to_response('mytalk/index.html',{'uid':uid,'hostStore':hostStore})

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
    return render_to_response('mytalk/showUserComments.html',{'uid':uid,'friend':friend,'talk':talk})
    
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

'''获得某一个商店的所有评论信息'''
def getStoreMessage(request):
    store = request.POST.get("store")
    if store != "":
        talk = getTheStoreMessage(store)
    else:
        talk = getCommonComments()
    return render_to_response('mytalk/showUserComments.html',{'talk':talk})

'''获得第几页的商店列表'''
def getStoreList(request):
    page = int(request.POST.get("page"))
    storeList = getPageStoreList(page)
    return render_to_response('mytalk/showStoreList.html',{'storeList':storeList})
	
'''商店是否存在，存在返回网页'''
def isStoreExist(request):
    store_name = request.POST.get('store')
    if is_store_exist(store_name):
        storeList = [store_name]
        return render_to_response('mytalk/showStoreList.html',{'storeList':storeList})
    return HttpResponse("")
    
'''插入新的商店'''
def insertNewStore(request):
    store_name = request.POST.get('storeName')
    store_place = request.POST.get('storePlace')
    if insert_new_store(store_name,store_place):
        storeList = [store_name]
        return render_to_response('mytalk/showStoreList.html',{'storeList':storeList})
    else:
        return HttpResponse("")
        
'''插入新的评论'''
def insertNewComment(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})
        
    comment = request.POST.get('comment')
    store_name = request.POST.get('store')
    uid = request.session.get('uid')
    visibility = int(request.POST.get('visibility'))
    
    if insert_new_comment(comment,store_name,uid,visibility):
        talk = getTheStoreMessage(store_name)
        return render_to_response('mytalk/showUserComments.html',{'talk':talk})
    else:
        return HttpResponse("")
    