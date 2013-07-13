将项目clone下来后，进行以下的修改  
1.修改/SmallTalk/setting.py中第15行的数据库文件路径，将其指向当前项目所存放位置的根目录下。  
2.修改/SmallTalk/setting.py中第114行的模板文件夹路径，将其指向当前项目所存放位置的根目录下的templates文件夹。  
3.运行python manage.py runner运行  
4.运行python manager.py syncdb建立数据库，并创建超级用户。  
