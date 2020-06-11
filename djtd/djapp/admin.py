from django.contrib import admin
from .models import Question
# Register your models here.

#管理页中添加投票系统
admin.site.register(Question)