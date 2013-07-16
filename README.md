#下载和安装


----------


将项目clone下来后，进行以下的修改：  

1. 修改/SmallTalk/setting.py中第**15**行的数据库文件路径，将其指向当前项目所存放位置的根目录下。
2. 修改/SmallTalk/setting.py中第**114**行的模板文件夹路径，将其指向当前项目所存放位置的根目录下的templates文件夹。
3. 运行**python manage.py runner**运行
4. 运行**python manager.py syncdb**建立数据库，并创建超级用户。

#提交项目


----------

1. 在自己的机子上生成ssh，并与自己的帐号关联，记住不是与公共仓库的帐号关联，因为已经在该项目将小组成员添加为贡献者了，所以只要与自己的帐号关联就行了。附权限问题的解决方案http://stackoverflow.com/questions/12940626/github-error-message-permission-denied-publickey 和官网教程：https://help.github.com/articles/generating-ssh-keys

2.  关于如何提交项目，涉及在公共仓库中**删除**和添加文件，参考以下网址：http://www.cnblogs.com/fnng/archive/2012/01/07/2315685.html 。需要注意的点是在push前要先pull下来，然后解决与公共仓库的代码冲突才能push上去。

#使静态文件生效


----------

参考网址：https://docs.djangoproject.com/en/1.5/intro/tutorial06/<br/>
1. 在想导入静态文件的文件的页面最上方添加{% load staticfiles %}<br/>
2. 将静态文件放在static文件夹中对应文件夹下<br/>

#关于Wiki Page


----------

1. 介绍和使用，http://www.worldhello.net/gotgithub/04-work-with-others/060-wiki.html 
2. Wiki Page使用的Markdown 语法说明：http://wowubuntu.com/markdown/
3. 建议先在一个Markdown的实时显示网站上写Page:http://benweet.github.io/stackedit/#
