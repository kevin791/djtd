from django.urls import path
from . import views

#为URL名称添加命名空间,方便项目中多应用的情况
app_name = 'djapp'

urlpatterns = [
    path('',views.index,name='index'),
    # #<int:question_id>捕获URL传入的整数型
    # path('<int:question_id>/',views.detail,name='detail'),
    #改变投票详情视图的URL
    path('specifics/<int:question_id>/',views.detail,name='detail'),
    path('<int:question_id>/results/',views.results,name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
]