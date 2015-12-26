# coding=utf8
from django.shortcuts import render,get_object_or_404
from .models import projectinfo
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    #获取projectinfo项目信息并分页显示
    fenyeno = 5
    objects = projectinfo.objects.filter(isinit=1)
    from .fenye import fenYe 

    posts,allPage,curPage = fenYe(request,fenyeno,objects)
    addno = fenyeno * (curPage - 1)
    lists = range(1,allPage+1)
    return render(request,'release/index.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})

@login_required
def release(request):
    #获取前端传递过来的项目id和预发布注释内容
    #username = request.session.get('username','anybody')
    username = request.user.username
    id = str(request.POST.get('id',''))
    comments = request.POST.get('comments','')
    reobj = projectinfo.objects.get(id=id)

    from release import release
    result = release(comments,reobj,username)

    json_result = {'id':str(id),'comments':comments,'result':result}
    return  HttpResponse(json.dumps(json_result,ensure_ascii=False))
