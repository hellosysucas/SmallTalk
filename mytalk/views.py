# Create your views here.
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from urllib import unquote
from django.template.loader import get_template
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
import hashlib
import datetime, re
import time
from django import forms
from django.http import HttpResponseRedirect
from mytalk.models import User,Store,Label,Comment,Reply,LabelInline,StoreAdmin

#添加好友
def become_my_friend(uid,friendName):
    return True

    
#获得某一个商店的所有评论信息,store 为商店名,最后返回一个只有一个元素的数组,方便函数重用,如果没有这个商店，返回一个空数组；同样每一页12个评论
def getTheStoreMessage(store,page):
    comment1 = ["good","very good","not bad","4"]
    author1 = ['tom1','tom2','tom3','tom4']
    theStore = {"name":store,"place":"guang zhou","comment":comment1,'author':author1}
    
    talk = [theStore]
    return talk

# initia and test database
def test(request):
    insert_new_store("test", "here")
    insert_new_store("test2", "there")
    insert_new_store("test3", "there")
    
    '''
    insert_new_comment("false", "test", "lc", False)
    insert_new_comment("true", "test", "lc", True)
    insert_new_comment("true2", "test2", "lc", True)
    insert_new_comment("true3", "test2", "mt", True)
    insert_new_comment("true4", "test2", "zp", True)
    '''
    
    return HttpResponse(getHostStore())
    #return HttpResponse(getCommonComments())

# initia and test database
def test(request):
    insert_new_store("test", "here")
    insert_new_store("test2", "there")
    insert_new_store("test3", "there")
    
    return HttpResponse(getFriendsSize("lc"))

    '''test is_my_friend
    User.objects.get(id = "mt").friends = User.objects.all()
    return HttpResponse( is_my_friend("mt", "lc"))
    '''
    
    '''test getUserComments getCommonComments getTheStoreMessage
    insert_new_comment("false", "test", "lc", False)
    insert_new_comment("1", "test", "lc", True)
    insert_new_comment("2", "test", "lc", True)
    insert_new_comment("3", "test", "lc", True)
    insert_new_comment("4", "test", "lc", True)
    insert_new_comment("5", "test", "lc", True)
    insert_new_comment("6", "test", "lc", True)
    insert_new_comment("7", "test", "lc", True)
    insert_new_comment("8", "test", "lc", True)
    insert_new_comment("9", "test", "lc", True)
    insert_new_comment("10", "test", "lc", True)
    insert_new_comment("11", "test", "lc", True)
    insert_new_comment("12", "test", "lc", False)
    insert_new_comment("12", "test", "lc", True)
    insert_new_comment("true2", "test2", "lc", True)
    insert_new_comment("true3", "test2", "mt", True)
    insert_new_comment("true4", "test2", "zp", True)
    insert_new_comment("true5", "test2", "zp", False)
    insert_new_comment("true6", "test2", "zp", False)

    
    #return  HttpResponse( getUserComments("lc", 1));
    #return  HttpResponse( getCommonComments( 1 ));
    return  HttpResponse( getTheStoreMessage("test", 0));
    '''
      
    '''test getFriendsList
    User.objects.get(id = "mt").friends = User.objects.all()
    return HttpResponse( getFriendsList("mt", 1))
    '''
    
#获得用户uid的好友列表,每个页面显示9个好友，page从0开始,没有好友返回空数组
def getFriendsList(uid,page):
    friends = []
    page = page * 9
    try:
        user = User.objects.get(id = uid)
        friendsList = user.friends.order_by("id")
        
        for i in friendsList:
            if i.id != uid:
                friends.append(i.id)
    except:
        print uid + "errors in getFriendsList"
    return friends[page : page + 9]

#获得好友人数
def getFriendsSize(uid):
    try:
        user = User.objects.get(id = uid)
        return len(user.friends.all())
    except:
        print "errors in getFriendsSize"
        return 0

#获得某个人的所有评论过的商店的所有评论,按照商店显示；页数代表每一页显示12条评论，第0也代表0~11的评论，第1页代表12~23的评论，以商店为单位
def getUserComments(uid,page):
    talk = []
    store_name = []
    result = []
    
    page = page * 12
    
    try:
        user = User.objects.get(id = uid)
        comment = user.comment_set.all()
        
        for item in comment:
            if store_name.count( item.store.name ) == 0:
                comment_tmp = [item.content]
                store = {"name": item.store.name, "place": item.store.place, "comment": comment_tmp}
                
                talk.append(store)
                store_name.append(item.store.name)
                
            else:
                index = store_name.index(item.store.name )
                talk[index]["comment"].append(item.content)
        
        num = 0
        for i in range( len(talk) ):
            tmp = {"name": talk[i]["name"], "place": talk[i]["place"], "comment": [] }
            for j in range ( len(talk[i]["comment"])) :
                if num >= page and num < page + 12:
                    tmp["comment"].append( talk[i]["comment"][j] )
                num += 1
            
            if len(tmp["comment"]) != 0:
                result.append(tmp)
            
            if num >= page + 12:
                break
                                  
    except:
        print "errors occurs in getUserComments"
    
    return result
    
#获得公开的所有商店的所有评论,注意，是公开显示的评论;每一页12个评论，第零页开始
def getCommonComments(page):
    talk = []
    store_name = []
    result = []
    
    page = page * 12
    
    try:
        comment = Comment.objects.filter(visible = True)
        
        for item in comment:
            if store_name.count( item.store.name ) == 0:
                comment_tmp = [item.content]
                store = {"name": item.store.name, "place": item.store.place, "comment": comment_tmp}
                talk.append(store)
                store_name.append(item.store.name)
            else:
                index = store_name.index(item.store.name )
                talk[index]["comment"].append(item.content)
                
        num = 0
        for i in range( len(talk) ):
            tmp = {"name": talk[i]["name"], "place": talk[i]["place"], "comment": [] }
            for j in range ( len(talk[i]["comment"])) :
                if num >= page and num < page + 12:
                    tmp["comment"].append( talk[i]["comment"][j] )
                num += 1
            
            if len(tmp["comment"]) != 0:
                result.append(tmp)
            
            if num >= page + 12:
                break
            
    except:
        print "errors occurs in getCommonComments"
    
    return result

#判断用户名是否格式合法
def is_uid_name_valid(uid):
    pattern = re.compile(r'[A-Za-z](\w|_| )*')
    
    if pattern.match(uid) and len(uid) <= 20:
        return True
    return False    
    
#判断邮箱格式是否合法
def is_email_name_valid(email):
    pattern = re.compile(r'\w*@(\w)+.(com|cn|org)')
    
    if pattern.match(email):
        return True
    return False

#判断密码是否合法
def is_password_valid(password):
    pattern = re.compile(r'\w+')
    
    if pattern.match(password):
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
def update_user_password(uid,password):
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

#判断某个用户名是否已经存在
def is_uid_exist(uid):
    try:
        user = User.objects.get(id = uid)
        return True
    except:
        return False

#判断用户是否合法,需要先验证uid和upassword是否为空等格式是否正确
def is_user_valid(uid,upassword):
    if is_uid_name_valid(uid) and is_password_valid(upassword) and is_uid_exist(uid):
        user = User.objects.get(id = uid)
        if user.password == upassword:
            return True
    return False

#判断某一个商店是否存在，传递过来的是商店名字符串
def is_store_exist(store_name):
    try:
        store = Store.objects.get(name = store_name)
        return True
    except:
        return False
    
#获得用户信息,包括用户邮箱Email
def getUserMessage(uid):
    try:
        user = User.objects.get(id = uid)
        return {'uid':user.id, 'email':user.email}
    except:
        return {'uid':uid, 'email':''}  

#插入一条新的评论，comment为评论内容，store_name为商店名，uid为用户，visibility为一个int类型的值，1代表公共可见，0代表好友可见
def insert_new_comment(comment,store_name,uid,visibility):
    try:
        user = User.objects.get(id = uid)
        store = Store.objects.get(name = store_name)
        comment = Comment(  author = user,
                            store = store,
                            pub_time = time.time(),
                            content = comment,
                            visible = visibility
                          )
        comment.save() 
        return True
    except:
        print "errors occurs in getCommonComments"
        return False

#判断friendName是否为uid的好友，true代表是好友关系
def is_my_friend(uid,friendName):
    try:
        user = User.objects.get(id = uid)
        if len( user.friends.filter(id = friendName) ) > 0:
            return True
        
    except:
        print "erros in is_my_friend"
    
    return False

#获取热门商店,以及评论
def getHostStore():
    talk = []
    stores = Store.objects.all()
    count = []
    
    for store_item in stores:
        count.append( { "store": store_item.name, "num": len( store_item.comment_set.all() )} )
       
    count.sort(key=lambda count: count["num"], reverse = True)
    
    i = 0
    while i <= 5 and i < len(count):
        store = Store.objects.get(name = count[i]["store"])
        comms = store.comment_set.all().filter(visible = True)
        comment1 = []
        
        for comment_item in comms:
            comment1.append(comment_item.content)
            
        tmp = {"name": store.name, "place": store.place, "comment": comment1}
        talk.append(tmp)
        i+=1
        
    return talk

#获得第page+1个四个商店名，例如第零页的四个商店名，第二页的四个商店名
def getPageStoreList(page):
    
    stores = Store.objects.order_by("name")
    page = page * 4
    storePage = stores[page : page+4]
    
    storeList = []
    for item in storePage:
        storeList.append(item.name)
    
    return storeList
    
#插入新的商店，插入成功返回true
def insert_new_store(store_name,store_place):
    
    try:
        if is_store_exist(store_name) == False:
            store = Store(name = store_name,
                          place = store_place,
                          checked = True
                          )
            store.save()
            return True
    except:
        print "errors occurs in insert_new_store"
    return False
    
#删除用户uid的好友friend
def deleteUserFriend(uid,friend):
    try:
        user = User.objects.get(id = uid)
        friend = User.objects.get(id = friend)
        user.friends.remove(friend)
        
        return True 
    except:
        print "errors occurs in deleteUserFriend"
    
    return False
    
#插入新的用户到数据库中，密码已经是加密后的
def insert_new_user(email,uid,password):
    try:
        if is_uid_exist(uid) == False:
            new_user = User(id = uid,
                            email = email,
                            password = password
                            )
            new_user.save()
            return True
    except:
        print "errors occurs in insert_new_user"
    return False

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
        friendsList = getFriendsList(uid,0)
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
    myFriendsObj = getFriendsList(uid,0)
    size = getFriendsSize(uid)
    return render_to_response('mytalk/friends.html',{'uid':uid,'friendsList':myFriendsObj,'size':size})
    
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
    page = int(request.POST.get('page'))
    
    talk = getUserComments(uid,page)
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
    page = int(request.POST.get('page'))
    if store != "":
        talk = getTheStoreMessage(store,page)
    else:
        talk = getCommonComments(page)
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
        talk = getTheStoreMessage(store_name,0)
        return render_to_response('mytalk/showUserComments.html',{'talk':talk})
    else:
        return HttpResponse("")
    
'''搜索好友'''
def searchFriend(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})

    uid = request.session.get('uid')
    friendName = request.POST.get('username')
    
    if is_my_friend(uid,friendName):
        myFriendsObj = [friendName]
        return render_to_response('mytalk/friendsOperate.html',{'friendsList':myFriendsObj})
    else:
        return HttpResponse("")
 
'''更新好友列表'''
def changeFriendsList(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})
    
    uid = request.session.get('uid')
    page = int(request.POST.get('page'))
    
    myFriendsObj = getFriendsList(uid, page)
    return render_to_response('mytalk/friendsOperate.html',{'friendsList':myFriendsObj})

'''处理搜索'''
def doSearch(request):
    if request.POST.get('content') == None:
        content = ""
    else:
        content = request.POST.get('content')
    
    uid = ''
    if request.session.get('uid') != None:
        uid = request.session.get('uid')
    message = []
    if content!="" and is_uid_name_valid(content):
        '''获得这个好友的评论'''    
        if uid!="" and is_my_friend(uid, content):
            talk = getUserComments(content, 0)
            if len(talk)>=2:
                comment = talk[0]['comment']
                for i in range(1,len(comment)):
                    comment.pop()
                comment2 = talk[1]['comment']
                for i in range(1,len(comment2)):
                    comment2.pop()
            else:
                comment = talk[0]['comment']
                for i in range(2,len(comment)):
                    comment.pop()
            message.append({'talk':talk,'type':'1'})
            
        if is_store_exist(content):
            talk1 = getTheStoreMessage(content, 0)
            comment1 = talk1[0]['comment']
            for i in range(2,len(comment1)):
                comment1.pop()
            message.append({'talk':talk1,'type':'0'})   
        return render_to_response('mytalk/search.html',{'message':message,'content':content})
    elif content == "":
        return render_to_response('mytalk/search.html')
    else:
        return HttpResponse("非法操作")

''''''
def changeShopState(request):
    store = request.POST.get('store')
    content = request.POST.get('content')
    talk = getTheStoreMessage(store, 0)
    #return HttpResponse(talk)
    return render_to_response('mytalk/userComments.html',{'talk':talk,'content':content})
    
''''''
def beFriend(request):
    uid = ''
    if request.session.get('uid') == None:
        return render_to_response('mytalk/index.html',{'uid':uid})
    
    friendName = request.POST.get('username')
    if is_my_friend(uid, friendName):
        return HttpResponse("已成为好友")
    else:
        become_my_friend(uid,friendName)
        return HttpResponse("成功添加")
    
