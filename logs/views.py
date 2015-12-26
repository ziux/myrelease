# coding=utf8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import json

@login_required
def sys(request):
    f = u'真的狠好'
    return render(request,'logs/sys.html',{'f':f})

@login_required
def release(request):
    from release.models import projectinfo
    from release.fenye import fenYe
    #查询项目列表列出项目(分页)
    fenyeno = 10
    objects = projectinfo.objects.filter(isinit=1)
    posts,allPage,curPage = fenYe(request,fenyeno,objects)
    addno = fenyeno * (curPage - 1)
    lists = range(1,allPage+1)
    result = {'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists}     
    
    return render(request,'logs/release.html',result)
    
        
   
@login_required
def relist(request,id):
    #点击项目 则列出该项目的发布历史记录(分页)
    from release.models import projectinfo
    ob = projectinfo.objects.filter(id=id).values("name")
    for o in ob:
        name = o['name']

    from release.models import release
    from release.fenye import fenYe
    objects = release.objects.filter(name=id).values("id","retime","restatus","releaser","comments").order_by("-id")
    
    fenyeno2 = 10
    posts2,allPage2,curPage2 = fenYe(request,fenyeno2,objects)
    addno2 = fenyeno2 * (curPage2 - 1)
    lists2 = range(1,allPage2+1)
    

 
    result = {'posts2':posts2,'allPage2':allPage2,'curPage2':curPage2,'addno2':addno2,'lists2':lists2,'proid':id,'name':name} 
    return render(request,'logs/relist.html',result)

   


@login_required
def relog(request,id,proid):
    #点击历史记录则显示详细的日志信息
    from release.models import projectinfo
    #proobj = projectinfo.objects.get(id=proid)
    #name = proobj.name
    
    ob = projectinfo.objects.filter(id=proid).values("name")
    for o in ob:
        name = o['name']
    
    from release.models import release
    objects = release.objects.filter(id=id).values("relog","retime")
    
    
    for o in objects:
        relog = o['relog']
        retime = o['retime']
    return render(request,'logs/relog.html',{'relog':relog,'name':name,'retime':retime})

