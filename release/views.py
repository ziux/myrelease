# coding=utf8
from django.shortcuts import render,get_object_or_404
from .models import projectinfo
from .models import permission
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    #username = request.user.username
    #分页一页多少条数据
    fenyeno = 10

    if request.user.is_superuser == True:
    #判断是否是管理员，是管理员则查询出所有项目
    #获取projectinfo项目信息并分页显示
        objects = projectinfo.objects.filter(isinit=1)
        from .fenye import fenYe 

        posts,allPage,curPage = fenYe(request,fenyeno,objects)
        addno = fenyeno * (curPage - 1)
        lists = range(1,allPage+1)
        return render(request,'release/index.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})
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
                    return render(request,'release/index.html')
                else:
                    from .fenye import fenYe
                    posts,allPage,curPage = fenYe(request,fenyeno,objects)
                    addno = fenyeno * (curPage - 1)
                    lists = range(1,allPage+1)
                    return render(request,'release/index.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})
                
            else:
                #该用户拥有项目列表为空则直接返回不查询
                return render(request,'release/index.html')
        else:
            #2：如果没有对应的名字则不显示任何项目
            return render(request,'release/index.html')





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
