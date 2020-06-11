from django.shortcuts import render
from django.http import HttpResponse
from .models import Question,Choice
from django.template import loader
from django.shortcuts import render
# Create your views here.
#第一个视图
# def index(request):
#     return HttpResponse("Hehllo,world.")
#实验访问多个页面-------------
def detail(request,question_id):
    return HttpResponse("You're looking at question %s." %question_id)

def results(request,question_id):
    response="you're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse("you're voting on question %s." % question_id)
#--------------------------
#真正有用的视图----------------
#我们在 index() 函数里插入了一些新内容，
# 让它能展示数据库里以发布日期排序的最近 5 个投票问题，以空格分割：
def index(request):
    #展示数据库里以发布日期排序的最近5个内容，以空格分隔
    #增删改查——查
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # #循环遍历输出数据前五条内容，以逗号分隔
    # output = ' , '.join([q.question_text for q in latest_question_list])
    template = loader.get_template('djapp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context,request))
#------------------------------