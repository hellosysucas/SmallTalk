#--*--coding: utf-8 --*--
from django.db import models
from mytalk.models import *
from django.contrib import admin
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