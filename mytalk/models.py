#-*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key = True, max_length = 20 )
    password = models.CharField(max_length = 20)
    email = models.EmailField()
    friends = models.ManyToManyField('self', null = True, blank = True, symmetrical=False)
    
    def __unicode__(self):
        return self.id

class Store(models.Model):
    name = models.CharField(max_length = 50)
    place = models.CharField(max_length = 100)
    checked = models.BooleanField()
    
    def __unicode__(self):
        return self.place+"   "+ self.name
    

class Label(models.Model):
    obj = models.ForeignKey(Store)
    name = models.CharField(max_length = 20)
    

class Comment(models.Model):
    author = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    pub_time = models.DateTimeField(auto_now = True)
    content = models.TextField()
    visible = models.BooleanField()
    def __unicode__(self):
        return self.author.id + "     " +self.content

class Reply(models.Model):
    obj = models.ForeignKey(Comment)
    author = models.ForeignKey(User)
    pub_time = models.DateTimeField(auto_now = True)
    content = models.TextField()

#系统管理员方便管理

#Store
class LabelInline(admin.TabularInline):
    model = Label
    extra = 0

class StoreAdmin(admin.ModelAdmin):
    inlines = [LabelInline]

admin.site.register(Store, StoreAdmin)

#User
admin.site.register(User)

#Comment
admin.site.register(Comment)