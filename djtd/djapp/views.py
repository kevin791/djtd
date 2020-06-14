from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Question,Choice
from django.template import loader
from django.shortcuts import render
# Create your views here.
#第一个视图
# def index(request):
#     return HttpResponse("Hehllo,world.")
#实验访问多个页面-------------
# def detail(request,question_id):
#     return HttpResponse("You're looking at question %s." %question_id)

# def results(request,question_id):
#     response="you're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request,question_id):
#     return HttpResponse("you're voting on question %s." % question_id)
#--------------------------
#真正有用的视图----------------
#我们在 index() 函数里插入了一些新内容，
# 让它能展示数据库里以发布日期排序的最近 5 个投票问题，以空格分割：
def index(request):
    #展示数据库里以发布日期排序的最近5个内容，以空格分隔
    #增删改查——查
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # #输出方式一：循环遍历输出数据前五条内容，以逗号分隔
    # output = ' , '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    #输出方式二：上下文字典传递映射对象
    # template = loader.get_template('djapp/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context,request))
    #输出方式三：render():django提供了一个用作【载入末班，填充上下文，再返回由它生成httpresponse对象】的函数
    context = {'latest_question_list':latest_question_list}
    return render(request,'djapp/index.html',context)

def detail(request,question_id):
    #这段代码有问题，Quwstion不能调用DoesNotExist异常
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("没有问题")
    # return render(request,'djapp/detail.html',{'question' : question})
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'djapp/detail.html',{'question': question})
#------------------------------