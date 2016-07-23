# coding=utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from release.models import projectinfo
from release.fenye import fenYe
from django.db import IntegrityError
from datetime import datetime

# Create your views here.


@login_required
def project_list(request):
    # 如果是管理员则显示项目列表
    if request.user.is_superuser is True:

        fenyeno = 10
        objects = projectinfo.objects.all()
        posts, allPage, curPage = fenYe(request, fenyeno, objects)
        addno = fenyeno * (curPage - 1)
        lists = range(1, allPage + 1)
        re = {'posts': posts, 'allPage': allPage,
              'curPage': curPage, 'addno': addno, 'lists': lists}
        return render(request, 'project/index.html', re)
    else:
        return HttpResponseRedirect('/')


@login_required
def edit_project(request, id):
    # 如果是管理员则允许编辑对应id的项目
    if request.user.is_superuser is True:

        editproject = projectinfo.objects.get(id=id)
        if request.method == "POST":
            try:
                editproject.name = request.POST['projectname']
                editproject.types = request.POST['types']
                editproject.isinit = int(request.POST['isinit'])
                editproject.save()

                return HttpResponseRedirect('/project/')
            except IntegrityError:

                msg = "修改失败！是不是项目名重复了?"
                re = {'id': id, 'editproject': editproject, 'msg': msg}
                return render(request, 'project/editproject.html', re)
        else:
            re = {'id': id, 'editproject': editproject}
            return render(request, 'project/editproject.html', re)
    else:
        return HttpResponseRedirect('/')


@login_required
def add_project(request):
    # 如果是管理员则允许添加项目
    if request.user.is_superuser is True:
        if request.method == "POST":
            # print(request.POST.get('projectname',''),request.POST.get('types',''),int(request.POST.get('isinit',0)))
            projectname = request.POST.get('projectname', '').strip()
            types = request.POST.get('types', '')
            isinit = int(request.POST.get('isinit', 0))
            if request.POST.get('projectname', '').strip() == '':
                msg = "添加失败，项目名称不能为空"
                return render(request, 'project/addproject.html', {'msg': msg})
            else:

                try:
                    r = projectinfo(
                        name=projectname,
                        lastretime=datetime.min,
                        types=types,
                        isinit=isinit)

                    r.save()
                    return HttpResponseRedirect('/project/')
                except IntegrityError:
                    msg = "添加失败！是不是项目名重复了?"
                    re = {'msg': msg}
                    return render(request, 'project/addproject.html', re)

        else:
            return render(request, 'project/addproject.html')
    else:
        return HttpResponseRedirect('/')
