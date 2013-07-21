#--*-- coding: utf-8 --*--

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from mytalk.models import *
from mytalk.views import *
        

#test is_uid_name_valid 函数
class UsernameTest(TestCase):
    def test_username_0(self):
        #用户名不能为空
        v0 = is_uid_name_valid("")
        self.assertFalse(v0)
        
    def test_username_1(self):
        #用户名只含有字母
        v1 = is_uid_name_valid("abcd")
        self.assertTrue(v1)
        
    def test_username_2(self):
        #用户名含有数字
        v2 = is_uid_name_valid("afd123")
        self.assertTrue(v2)
        
    def test_username_3(self):
        #用户名含有特殊字符
        v3 = is_uid_name_valid("abcx!?")
        self.assertTrue(v3)
        
    def test_username_4(self):
        #长度超过20个字符
        v4 = is_uid_name_valid("abcxasdfasdfasdfjkzxcvzlxjvklernfknsvkjskdfnvnk")
        self.assertFalse(v4)
    

#test is_email_name_valid 函数
class EmailTest(TestCase):
    def test_email_0(self):
        #合法的email
        em0 = is_email_name_valid("23413241@qq.com")
        self.assertTrue(em0)
        
    def test_email_1(self):
        #两个@
        em1 = is_email_name_valid("2341@3241@qq.com")
        self.assertFalse(em1)
        
    def test_email_2(self):
        #不合法的后缀
        em2 = is_email_name_valid("23413241@qq.afdaf")
        self.assertFalse(em2)
        
        
    def test_email_3(self):
        #@和.之间没有字符
        em3 = is_email_name_valid("23413241@.com")
        self.assertFalse(em3)


#test is_password_valid 函数
class PasswordTest(TestCase):
    def test_password_0(self):
        #密码为空
        pw = is_password_valid("")
        self.assertFalse(pw)
    
    def test_password_1(self):
        #密码含有特殊字符
        pw = is_password_valid("adsf@!?")
        self.assertTrue(pw)
    
    def test_password_2(self):
        #超长密码
        pw = is_password_valid("adsfjkasdnfkahdfiu239828349hdsiohfadsfnjkasfhu29ufsd")
        self.assertTrue(pw)


#test is_uid_exist 函数
class IsUidExist(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        
    def test_0(self):
        #id存在
        self.assertTrue(is_uid_exist('user1'))
    
    def test_1(self):
        #id不存在
        self.assertFalse(is_uid_exist('user2'))
        
        
#test update_user_id 函数
class UpdateUserIdTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1')
        User.objects.create(id='user2', password='user2')
        
    def test_0(self):
        #user1换成一个不存在的id
        res = update_user_id('user1', 'user3')
        self.assertTrue(res)
        if not is_uid_exist('user1') and is_uid_exist('user3'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
    def test_1(self):
        #user1换成一个已经存在的id
        res = update_user_id('user1', 'user2')
        self.assertFalse(res)
    
    def test_2(self):
        #被更新的用户不存在
        res = update_user_id('user0', 'user3')
        self.assertFalse(res)
        
        
    def test_3(self):
        #新的用户名不合法
        res = update_user_id('user1', 'adsfvczc234309zvdijkvnkwejfiio0987z97v8z7v9z0v0')
        self.assertFalse(res)
    

#test update_user_email 函数
class UpdateUserEmailTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='123456@qq.com')
        User.objects.create(id='user2', password='user2', email='987654@qq.com')
        
    def test_0(self):
        #user不存在
        res = update_user_email('user0', 'user0@qq.com')
        self.assertFalse(res)
        
    def test_1(self):
        #email不合法
        res = update_user_email('user1', 'user1sfdas.com')
        self.assertFalse(res)
    
    def test_2(self):
        #均合法
        res = update_user_email('user1', 'user1@qq.com')
        self.assertTrue(res)
        user = User.objects.get(id='user1')
        self.assertEquals(user.email, 'user1@qq.com')


#test update_user_password 函数
class UpdateUserPasswordTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
        User.objects.create(id='user2', password='user2', email='user2@qq.com')
        
    def test_0(self):
        #user不存在
        res = update_user_password('user0', '1234')
        self.assertFalse(res)
        
    def test_1(self):
        #password不合法
        res = update_user_password('user1', '')
        self.assertFalse(res)
    
    def test_2(self):
        #均合法
        res = update_user_password('user1', '1234')
        self.assertTrue(res)
        user = User.objects.get(id='user1')
        self.assertEquals(user.password, '1234')


#test is_user_valid 函数
class IsUserValidTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
        
    def test_0(self):
        #用户不合法
        self.assertFalse( is_user_valid('user0', '134141'))
    
    def test_1(self):
        #用户密码不正确
        self.assertFalse( is_user_valid('user1', '134141'))
    
    def test_2(self):
        #合法
        self.assertTrue( is_user_valid('user1', 'user1'))


#test is_store_exist 函数
class IsStoreExistTest(TestCase):
    def setUp(self):
        Store.objects.create(name='store1', place='asfdasdfas', checked=True)
    
    def test_0(self):
        #商户不存在
        self.assertFalse( is_store_exist('store0'))
    
    def test_1(self):
        #商户存在
        self.assertTrue( is_store_exist('store1') )


#test getUserMessage 函数
class GetUserMessageTest(TestCase):
    def setUp(self):
        User.objects.create(id='user1', password='user1', email='user1@qq.com')
    
    def test_0(self):
        #用户不存在
        dic = getUserMessage('user0')
        if dic:
            self.assertTrue(True)
        else:
            self.assertTrue(True)

    def test_1(self):
        #返回email
        dic = getUserMessage('user1')
        if dic and dic['email']== 'user1@qq.com':
            self.assertTrue(True)
        else:
            self.assertFalse(True)


#test getFriendsList 函数
class GetFriendsListTest(TestCase):
    
    pass


#test getUserComments 函数
class GetUserComments(TestCase):
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
        #用户名不存在
        comments = getUserComments('user1')
        self.assertEquals(len(comments), 0)
    
    def test_1(self):
        #获取所有评论
        comments = getUserComments('user')
        self.assertEquals(len(comments), 2)
        self.assertEquals(len(comments[0]['comment']), 2)
        comments = getUserComments('user2')
        self.assertEquals(len(comments), 1)


#test getCommonComments 函数
class GetCommonComments(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        User.objects.create(id='user2', password='user2')
        Store.objects.create(name='store', place='abc', checked=True)
        Store.objects.create(name='store1', place='abczxcv', checked=True)
        content = 'asdfanzmxvaosi'
        insert_new_comment(content, 'store', 'user', True)
        insert_new_comment(content, 'store', 'user', False)
        
    def test_0(self):
        insert_new_comment('vsdfge', 'store1', 'user2', True)
        comments = getCommonComments()
        self.assertEquals(len(comments), 2)
    
    def test_1(self):
        insert_new_comment('zxcver', 'store1', 'user', False)
        comments = getCommonComments()
        self.assertEquals(len(comments), 1)

#test insert_new_comment 函数
class InsertNewCommentTest(TestCase):
    def setUp(self):
        User.objects.create(id='user', password='user')
        Store.objects.create(name='store', place='abc', checked=False)
        
    def test_0(self):
        #正常添加一条评论
        user = User.objects.get(id = 'user')
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
        #商户不存在或者用户不存在
        user = User.objects.get(id = 'user')
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 0)
        content = 'adsfafdasdfaddfsa'
        suc = insert_new_comment(content, 'store1', 'user', True)
        self.assertFalse(suc)
        suc = insert_new_comment(content, 'store', 'user1', True)
        self.assertFalse(suc)

    def test_2(self):
        #测试可见性
        user = User.objects.get(id = 'user')
        comments = user.comment_set.all()
        self.assertEquals(len(comments), 0)
        content = 'adsfafdasdfaddfsa'
        suc = insert_new_comment(content, 'store', 'user', True)
        self.assertTrue(suc)
        comments = user.comment_set.all()
        self.assertTrue(comments[0].visible )
        suc = insert_new_comment(content, 'store', 'user', False)
        self.assertTrue(suc)
        comments = user.comment_set.all()
        self.assertFalse(comments[1].visible )










