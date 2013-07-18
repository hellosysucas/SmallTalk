#下载和安装


----------


将项目clone下来后，进行以下的修改：  

1. 修改/SmallTalk/setting.py中第**15**行的数据库文件路径，将其指向当前项目所存放位置的根目录下。
2. 修改/SmallTalk/setting.py中第**114**行的模板文件夹路径，将其指向当前项目所存放位置的根目录下的templates文件夹。
3. 运行**python manage.py runner**运行
4. 运行**python manager.py syncdb**建立数据库，并创建超级用户。

#更新项目


----------
1. 了解git pull和git fetch的区别，参考网址：
http://my.oschina.net/zimingforever/blog/68621
2. 简而言之，git pull会自动帮你merge，而git fetch需要自己merge，所以大家都使用git fetch来更新项目，这样才能知道别人改了什么。具体命令：
> git fetch origin master:tmp  
> git diff tmp   
> git merge tmp


意思是从远程获取最新的版本到本地的test分支上之后再进行比较合并

#提交项目


----------

1. 在自己的机子上生成ssh，并与自己的帐号关联，记住不是与公共仓库的帐号关联，因为已经在该项目将小组成员添加为贡献者了，所以只要与自己的帐号关联就行了。附权限问题的解决方案http://stackoverflow.com/questions/12940626/github-error-message-permission-denied-publickey 和官网教程：https://help.github.com/articles/generating-ssh-keys

2.  关于如何提交项目，涉及在公共仓库中**删除**和添加文件，参考以下网址：http://www.cnblogs.com/fnng/archive/2012/01/07/2315685.html 。需要注意的点是在push前要先pull下来，然后解决与公共仓库的代码冲突才能push上去。

#使静态文件生效


----------

1. 参考网址：https://docs.djangoproject.com/en/1.5/intro/tutorial06/
2. 在想导入静态文件的文件的页面最上方添加{% load staticfiles %}
3. 将静态文件放在static文件夹中对应文件夹下
4. 举例：`<link href="{% static 'mytalk/css/bootstrap.css' %}" rel="stylesheet">`

#关于Wiki Page


----------

1. 介绍和使用，http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html 
2. Wiki Page使用的Markdown 语法说明：http://wowubuntu.com/markdown/
3. 建议先在一个Markdown的实时显示网站上写Page:http://benweet.github.io/stackedit/#

#接下来的任务


----------

1. 爬取大众点评的相关数据，填充数据库，考虑到时间关系，可手工收集
2. 实现首页上各个控件的点击及页面跳转
  * 填充商店名和评论以及细节显示
	* 实现添加点评功能
	* 在首页增加添加点评时的选择可见性和商户功能
	* 在好友圈显示好友列表
	* 在热门点评商户显示商户列表
3. 添加商户信息页面
4. 优化好友管理页面
5. 优化用户信息管理页面
6. 优化系统管理页面
7. 增加测试
8. 挂载服务器
9. 撰写文档
10. 提交到Soya 
