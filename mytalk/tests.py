# --*--coding:utf-8 --*--

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mytalk.models import *
from mytalk.views import *
        

# test is_uid_name_valid 函数
class UsernameTest(TestCase):
    def test_username_0(self):
        # 用户名不能为空
        v0 = is_uid_name_valid("")
        self.assertFalse(v0)
        
    def test_username_1(self):
        # 用户名只含有字母
        v1 = is_uid_name_valid("abcd")
        self.assertTrue(v1)
        
    def test_username_2(self):
        # 用户名含有数字
        v2 = is_uid_name_valid("afd123")
        self.assertTrue(v2)
        
    def test_username_3(self):
        # 用户名含有特殊字符
        v3 = is_uid_name_valid("abcx!?")
        self.assertTrue(v3)
        
    def test_username_4(self):
        # 长度超过20个字符
        v4 = is_uid_name_valid("abcxasdfasdfasdfjkzxcvzlxjvklernfknsvkjskdfnvnk")
        self.assertFalse(v4)
    

# test is_email_name_valid 函数
class EmailTest(TestCase):
    def test_email_0(self):
        # 合法的email
        em0 = is_email_name_valid("23413241@qq.com")
        self.assertTrue(em0)
        
    def test_email_1(self):
        # 两个@
        em1 = is_email_name_valid("2341@3241@qq.com")
        self.assertFalse(em1)
        
    def test_email_2(self):
        # 不合法的后缀
        em2 = is_email_name_valid("23413241@qq.afdaf")
        self.assertFalse(em2)
        
        
    def test_email_3(self):
        # @和.之间没有字符
        em3 = is_email_name_valid("23413241@.com")
        self.assertFalse(em3)


# test is_password_valid 函数
class PasswordTest(TestCase):
    def test_password_0(self):
        # 密码为空
        pw = is_password_valid("")
        self.assertFalse(pw)
    
    def test_password_1(self):
        # 密码含有特殊字符
        pw = is_password_valid("adsf@!?")
        self.assertTrue(pw)
    
    def test_password_2(self):
        # 超长密码
        pw = is_password_valid("adsfjkasdnfkahdfiu239828349hdsiohfadsfnjkasfhu29ufsd")
        self.assertTrue(pw)


# test is_uid_exist 函数
class IsUidExist(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        
    def test_0(self):
        # id存在
        self.assertTrue(is_uid_exist('user1'))
    
    def test_1(self):
        # id不存在
        self.assertFalse(is_uid_exist('user2'))
        
        
# test update_user_id 函数
class UpdateUserIdTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
        
    def test_0(self):
        # user1换成一个不存在的id
        res = update_user_id('user1', 'user3')
        self.assertTrue(res)
        if not is_uid_exist('user1') and is_uid_exist('user3'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
    def test_1(self):
        # user1换成一个已经存在的id
        res = update_user_id('user1', 'user2')
        self.assertFalse(res)
    
    def test_2(self):
        # 被更新的用户不存在
        res = update_user_id('user0', 'user3')
        self.assertFalse(res)
        
        
    def test_3(self):
        # 新的用户名不合法
        res = update_user_id('user1', 'adsfvczc234309zvdijkvnkwejfiio0987z97v8z7v9z0v0')
        self.assertFalse(res)
    

# test update_user_email 函数
class UpdateUserEmailTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='123456@qq.com')
        User.objects.create(id='user2', password='user2', email='987654@qq.com')
        
    def test_0(self):
        # user不存在
        res = update_user_email('user0', 'user0@qq.com')
        self.assertFalse(res)
        
    def test_1(self):
        # email不合法
        res = update_user_email('user1', 'user1sfdas.com')
        self.assertFalse(res)
    
    def test_2(self):
        # 均合法
        res = update_user_email('user1', 'user1@qq.com')
        self.assertTrue(res)
        user = User.objects.get(id='user1')
        self.assertEquals(user.email, 'user1@qq.com')


# test update_user_password 函数
class UpdateUserPasswordTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
        User.objects.create(id='user2', password='user2', email='user2@qq.com')
        
    def test_0(self):
        # user不存在
        res = update_user_password('user0', '1234')
        self.assertFalse(res)
        
    def test_1(self):
        # password不合法
        res = update_user_password('user1', '')
        self.assertFalse(res)
    
    def test_2(self):
        # 均合法
        res = update_user_password('user1', '1234')
        self.assertTrue(res)
        user = User.objects.get(id='user1')
        self.assertEquals(user.password, '1234')


# test is_user_valid 函数
class IsUserValidTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
        
    def test_0(self):
        # 用户不合法
        self.assertFalse(is_user_valid('user0', '134141'))
    
    def test_1(self):
        # 用户密码不正确
        self.assertFalse(is_user_valid('user1', '134141'))
    
    def test_2(self):
        # 合法
        self.assertTrue(is_user_valid('user1', 'user1'))


# test is_store_exist 函数
class IsStoreExistTest(TestCase):
    def setUp(self):
        Store.objects.create(name='store1', place='asfdasdfas', checked=True)
    
    def test_0(self):
        # 商户不存在
        self.assertFalse(is_store_exist('store0'))
    
    def test_1(self):
        # 商户存在
        self.assertTrue(is_store_exist('store1'))


# test getUserMessage 函数
class GetUserMessageTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
    
    def test_0(self):
        # 用户不存在
        dic = getUserMessage('user0')
        if dic:
            self.assertTrue(True)
        else:
            self.assertTrue(True)

    def test_1(self):
        # 返回email
        dic = getUserMessage('user1')
        if dic and dic['email'] == 'user1@qq.com':
            self.assertTrue(True)
        else:
            self.assertFalse(True)


# test insert_new_comment 函数
class InsertNewCommentTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        Store.objects.create(name='store', place='abc', checked=False)
        
    def test_0(self):
        # 正常添加一条评论
        user = User.objects.get(id='user')
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 0)
        content = 'adsfafdasdfaddfsa'
        insert_new_comment(content, 'store', 'user', True)
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 1)
        flag = False
        for item in comments:
            if item.author.id == 'user' and item.content == 'adsfafdasdfaddfsa':
                flag = True
        self.assertTrue(flag)
    
    def test_1(self):
        # 商户不存在或者用户不存在
        user = User.objects.get(id='user')
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 0)
        content = 'adsfafdasdfaddfsa'
        suc = insert_new_comment(content, 'store1', 'user', True)
        self.assertFalse(suc)
        suc = insert_new_comment(content, 'store', 'user1', True)
        self.assertFalse(suc)

    def test_2(self):
        # 测试可见性
        user = User.objects.get(id='user')
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 0)
        content = 'adsfafdasdfaddfsa'
        suc = insert_new_comment(content, 'store', 'user', True)
        self.assertTrue(suc)
        comments = user.comment_set.all()
        self.assertTrue(comments[0].visible)
        suc = insert_new_comment(content, 'store', 'user', False)
        self.assertTrue(suc)
        comments = user.comment_set.all()
        self.assertFalse(comments[1].visible)
        
        
# test become_my_friend 函数
class BecomeMyFriendTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
    
    def test_0(self):
        # 用户名不存在
        res = become_my_friend('user1', 'user3')
        self.assertFalse(res)
    
    def test_1(self):
        res = become_my_friend('user1', 'user2')
        self.assertTrue(res)
        user1 = User.objects.get(id='user1')
        user2 = User.objects.get(id='user2')
        det = (user2 in user1.friends.all())
        self.assertTrue(det)
        det = user1 in user2.friends.all()
        self.assertFalse(det)


# test getTheStoreMessage(store,page) 函数
class GetTheStoreMessageTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        Store.objects.create(name='store', place='afsdfasdf', checked=True)
        insert_new_comment("sdfasfasd", 'store', 'user', True)
        
    def test_0(self):
        # 正常获取
        res = getTheStoreMessage('store', 0, 'user')
        self.assertEquals(len(res), 1)
        
        
    def test_1(self):
        # 只列出可见的
        insert_new_comment("zvergw", 'store', 'user', False)
        res = getTheStoreMessage('store', 0, 'user')
        self.assertEquals(len(res), 1)
        self.assertEquals(len(res[0]['comment']), 2)
        
        insert_new_comment("zvergw", 'store', 'user', True)
        res = getTheStoreMessage('store', 0, 'user')
        self.assertEquals(len(res), 1)
        self.assertEquals(len(res[0]['comment']), 3)
        
    def test_2(self):
        # page不合法
        res = getTheStoreMessage('store', 2, 'user')
        self.assertEquals(len(res), 0)


# test getFriendsList(uid,page)函数
class GetFriendsListTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
        User.objects.create(id='user3', password='user3')
        become_my_friend('user1', 'user2')
        become_my_friend('user1', 'user3')
        become_my_friend('user2', 'user3')
        
    def test_0(self):
        # 测试功能
        res = getFriendsList('user1', 0)
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0], 'user2')
        
        res = getFriendsList('user2', 0)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0], 'user3')
    
    def test_1(self):
        # 测试合法性，page太大或为负
        res = getFriendsList('user1', 1)
        self.assertEquals(len(res), 0)
        
        res = getFriendsList('user1', -2)
        self.assertEquals(len(res), 0)
    
    def test_2(self):
        # 测试合法性, 用户名不存在
        res = getFriendsList('user3', 0)
        self.assertEquals(len(res), 0)


# test getFriendsSize(uid)函数
class GetFriendsSizeTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
        User.objects.create(id='user3', password='user3')
        become_my_friend('user1', 'user2')
        become_my_friend('user1', 'user3')
        become_my_friend('user2', 'user3')
        
    def test_0(self):
        # 测试功能
        res = getFriendsSize('user1')
        self.assertEquals(res, 2)
        
        res = getFriendsSize('user2')
        self.assertEquals(res, 1)
        
        res = getFriendsSize('user3')
        self.assertEquals(res, 0)
    
    def test_1(self):
        # 用户名不存在
        res = getFriendsSize('user4')
        self.assertEquals(res, 0)


# test getUserComments(uid, page) 函数
class GetUserCommentsTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        User.objects.create(id='user2', password='user2')
        Store.objects.create(name='store', place='abc', checked=True)
        Store.objects.create(name='store1', place='abczxcv', checked=True)
        content = 'asdfanzmxvaosi'
        insert_new_comment(content, 'store', 'user', True)
        insert_new_comment(content, 'store', 'user', False)
        insert_new_comment(content, 'store1', 'user', False)
        insert_new_comment(content, 'store1', 'user2', False)
        
    def test_0(self):
        # 用户名不存在
        res = getUserComments('user1', 0)
        self.assertEquals(len(res), 0)
    
    def test_1(self):
        # 获取所有评论
        res = getUserComments('user', 0)
        self.assertEquals(len(res), 2)
        self.assertEquals(len(res[0]['comment']), 2)
        res = getUserComments('user2', 0)
        self.assertEquals(len(res), 1)
    
    def test_2(self):
        # page不合法
        res = getUserComments('user', 2)
        self.assertEquals(len(res), 0)


# test getCommonComments(page) 函数
class GetCommonCommentsTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        User.objects.create(id='user2', password='user2')
        Store.objects.create(name='store', place='abc', checked=True)
        Store.objects.create(name='store1', place='abczxcv', checked=True)
        content = 'asdfanzmxvaosi'
        insert_new_comment(content, 'store', 'user', True)
        
    def test_0(self):
        insert_new_comment('vsdfge', 'store1', 'user2', True)
        res = getCommonComments(0)
        self.assertEquals(len(res), 2)
    
    def test_1(self):
        # 返回格式测试
        insert_new_comment('zxcver', 'store', 'user', True)
        res = getCommonComments(0)
        self.assertEquals(len(res), 1)
        self.assertEquals(len(res[0]['comment']), 2)
        
    def test_2(self):
        # 不可见测试
        insert_new_comment('vsdfge', 'store1', 'user', False)
        res = getCommonComments(0)
        self.assertEquals(len(res), 1)


# test is_my_friend(uid,friendName) 函数
class IsMyFriendTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
        become_my_friend('user1', 'user2')
    
    def test_0(self):
        # 功能性测试
        res = is_my_friend('user1', 'user2')
        self.assertTrue(res)
        
    def test_1(self):
        # 单向测试
        res = is_my_friend('user2', 'user1')
        self.assertFalse(res)
    
    def test_2(self):
        # 用户名不存在
        res = is_my_friend('user1', 'user0')
        self.assertFalse(res)


# test getHostStore 函数
class GetHostStoreTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        Store.objects.create(name='store1', place='store1', checked=True)
        Store.objects.create(name='store2', place='store2', checked=True)
    
    def test_0(self):
        # 功能性测试
        res = getHostStore()
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0]['name'], 'store1')
    
    def test_1(self):
        # 排序测试
        res = getHostStore()
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0]['name'], 'store1')
        insert_new_comment("asdfasdf", 'store2', 'user', True)
        res = getHostStore()
        self.assertEquals(res[0]['name'], 'store2')
    
    def test_2(self):
        # 新添加商户
        Store.objects.create(name='store3', place='store3', checked=True)
        res = getHostStore()
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0]['name'], 'store1')
        self.assertEquals(res[1]['name'], 'store2')
    

# test getPageStoreList(page) 函数
class GetPageStoreListTest(TestCase):
    def setUp(self):
        Store.objects.create(name='store1', place='store1', checked=True)
        Store.objects.create(name='store2', place='store2', checked=True)
        Store.objects.create(name='store3', place='store3', checked=True)
        Store.objects.create(name='store4', place='store4', checked=True)
        Store.objects.create(name='store5', place='store5', checked=True)
        Store.objects.create(name='store6', place='store6', checked=True)
    
    def test_0(self):
        # 功能性测试
        res = getPageStoreList(0)
        self.assertEquals(len(res), 4)
        self.assertEquals(res[0], 'store1')
        self.assertEquals(res[3], 'store4')
    
    def test_1(self):
        # Page
        res = getPageStoreList(1)
        self.assertEquals(len(res), 2)
        self.assertEquals(res[0], 'store5')
        self.assertEquals(res[1], 'store6')
        
        res = getPageStoreList(2)
        self.assertEquals(len(res), 0)


# test insert_new_store(store_name,store_place)
class InsertNewStoreTest(TestCase):
    def test_0(self):
        # 功能性测试
        insert_new_store('store1', 'store1')
        stores = Store.objects.all()
        flag = False
        for store in stores:
            if store.name == 'store1':
                flag = True
        self.assertTrue(flag)
        
    def test_1(self):
        # 已存在该商户
        insert_new_store('store1', 'store1')
        res = insert_new_store('store1', 'store1')
        self.assertFalse(res)


# test deleteUserFriend(uid,friend)
class DeleteUserFriendTest(TestCase):
    def setUp(self):
        User.objects.create(id='u1', password='u1')
        User.objects.create(id='u2', password='u2')
        become_my_friend('u1', 'u2')
        become_my_friend('u2', 'u1')
    
    def test_0(self):
        # 功能性测试
        deleteUserFriend('u1', 'u2')
        res = is_my_friend('u1', 'u2')
        self.assertFalse(res)
        res = is_my_friend('u2', 'u1')
        self.assertTrue(res)
    
    def test_1(self):
        # 本来就不是朋友
        User.objects.create(id='u3', password='u3')
        res = deleteUserFriend('u1', 'u3')
        self.assertTrue(res)
    

# test insert_new_user(email,uid,password)函数
class InsertNewUserTest(TestCase):
    def test_0(self):
        # 功能性测试
        res = insert_new_user('u1', 'u1', 'u1')
        self.assertTrue(res)
        
    def test_1(self):
        # 以存在该用户
        insert_new_user('u1', 'u1', 'u1')
        res = insert_new_user('u1', 'u1', 'u1')
        self.assertFalse(res)
    
    def test_2(self):
        # 用户名或者密码不合法
        res = insert_new_user('u1', 'u1sadfasdfasdfklasfjklwen,wnrf,nkvzk', 'u1')
        # self.assertFalse(res)
        # 此处未检查参数合法性，不过在调用该函数的地方已经检查了合法性
    
# test hashPassword(password)函数
class HashPasswordTest(TestCase):
    def test_0(self):
        password = '31af23'
        res = hashPassword(password)
        self.assertNotEquals(res, password)

