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
    from release.models import permission


    #分页一页多少条数据
    fenyeno = 10

    if request.user.is_superuser == True:
    #判断是否是管理员，是管理员则查询出所有项目
    #获取projectinfo项目信息并分页显示
        objects = projectinfo.objects.filter(isinit=1)
        posts,allPage,curPage = fenYe(request,fenyeno,objects)
        addno = fenyeno * (curPage - 1)
        lists = range(1,allPage+1)
        return render(request,'logs/release.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})
    else:
        #如果不是管理员，则根据名字去permission表查询有那些项目权限，
        ownpid = permission.objects.filter(username_id=request.user.username)
        if ownpid:
            #1：如果有对应名字则获取对应的项目id数组，通过这个数组再过滤是否改项目是启用状态
            for i in ownpid:
                prostr = str(i.ownprojectid).strip()
                
            print(prostr)
            if prostr:
                #该用户拥有项目列表非空则查询出项目
                prolist = filter(None,prostr.split(','))
                print(prolist)
                try:
                    objects = projectinfo.objects.filter(isinit=1,id__in=prolist)
                except ValueError:
                    return render(request,'logs/release.html')
                else:
                    posts,allPage,curPage = fenYe(request,fenyeno,objects)
                    addno = fenyeno * (curPage - 1)
                    lists = range(1,allPage+1)
                    return render(request,'logs/release.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})
                
            else:
                #该用户拥有项目列表为空则直接返回不查询
                return render(request,'logs/release.html')
        else:
            #2：如果没有对应的名字则不显示任何项目
            return render(request,'logs/release.html')
    
        
   
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
    if int(curPage2-3) < 0:
        fenyeqian = 0
    else:
        fenyeqian=int(curPage2-3)
    fenyehou=int(curPage2+2)
    fenyelist = lists2[fenyeqian:fenyehou] 
    print(curPage2)
    print(fenyelist)

 
    result = {'posts2':posts2,'allPage2':allPage2,'curPage2':curPage2,'addno2':addno2,'lists2':lists2,'proid':id,'name':name,'fenyelist':fenyelist} 
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

