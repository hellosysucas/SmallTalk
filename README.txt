现在已经配置好了js和css

添加了登录主页，但是并未进行验证，验证部分需要后台人员编写

在mytalk中，views.py，用引号注释的部分已经编写完毕，无需修改，只需要后台人员修改用#注释的部分

添加了用户信息修改页面，在最上面点击用户id后，即可跳转

其中，主页的编写放在了模版templates文件夹下的mainPage.html中，只需要编写这一个HTML文件即可

（注意在自己的linux环境下一定要修改settings.py中sqlite3和templates路径）