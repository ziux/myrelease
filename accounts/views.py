# coding=utf8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

def login_index(request):
    if not request.user.is_authenticated():
        return render(request, 'accounts/login.html')
    else:
        return HttpResponseRedirect('/index/')

def login_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #request.session['username'] = username
                request.session.set_expiry(14400)
                return HttpResponseRedirect('/')
            else:
                err = "用户没激活"
                return render(request, 'accounts/login.html', {'err': err})
        else:
            err = "用户密码错误"
            return render(request, 'accounts/login.html', {'err': err})
    else:
        return HttpResponseRedirect('/')



def logout_account(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_list(request):
    objects = User.objects.all()
    from release.fenye import fenYe
    fenyeno = 10

    posts,allPage,curPage = fenYe(request,fenyeno,objects)
    addno = fenyeno * (curPage - 1)
    lists = range(1,allPage+1)
    return render(request,'accounts/userlist.html',{'posts':posts,'allPage':allPage,'curPage':curPage,'addno':addno,'lists':lists})
    
@login_required
def user_add(request):
    if request.user.is_superuser is True:
        #开启表单提交并写入数据库
        if request.method == 'POST':
            first_name = request.POST['first_name']
            username = request.POST['username']
            password = request.POST['password']
            if username.strip()  == '' or password.strip() == '':
                err = "用户和密码不能为空"
                return render(request, 'accounts/useradd.html', {'err': err})
            else:
                #查用户名是否已经存在
                try:
                    objects = User.objects.get(username=username)
                    err = "用户存在，不创建"
                    return render(request, 'accounts/useradd.html', {'err': err})
                except User.DoesNotExist:
                    #不存在则开始创建用户
                    user = User.objects.create_user(username=username,password=password)
                    user.first_name=first_name
                    user.save()
                    #err = "创建用户成功"
                    #return render(request, 'accounts/useradd.html', {'err': err})
                    return HttpResponseRedirect('/accounts/user_list/')
        return render(request,'accounts/useradd.html')
    else:
        return render(request,'index/index.html')

@login_required
def user_edit(request,id):
    if request.user.is_superuser is True:
        edituser = User.objects.get(id=id)
        if request.method == "POST":
            #做判断，如果是super则只允许root和自己修改，
            if request.user.username == request.POST['username'] or request.user.username == 'root' or edituser.is_superuser == False:
                usersave(request,edituser)
                msg = "修改成功"
                return render(request,'accounts/useredit.html',{'id':id,'msg':msg,'edituser':edituser})
            else:
                #不允许修改其它管理员用户
                msg = "您不允许修改其它管理员用户"
                return render(request,'accounts/useredit.html',{'id':id,'msg':msg,'edituser':edituser})
        else:
            return render(request,'accounts/useredit.html',{'id':id,'edituser':edituser})
    else:
        return HttpResponseRedirect('/')


def usersave(request,edituser):
    edituser.first_name=request.POST['name']
    edituser.email=request.POST['Email']
    edituser.is_superuser=int(request.POST['is_superuser'])
    edituser.is_active=int(request.POST['is_active'])
    edituser.save()

@login_required
def user_edit_password(request,id):
    if request.user.is_superuser is True:
        cpuser = User.objects.get(id=id)
        if request.method == "POST":
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            if password1.strip()  != password2.strip():
                msg = "重置失败，两次输入的密码不一致"
                return render(request,'accounts/usereditpassword.html',{'id':id,'msg':msg})
            else:
                if cpuser.check_password(password1) == True:
                    msg = "不能和旧密码一致"
                    return render(request,'accounts/usereditpassword.html',{'id':id,'msg':msg})
                else:
                    #只能修改自己或者其它普通用户
                    if cpuser.is_superuser is False or cpuser.username == request.user.username or request.user.username=='root':
                        cpuser.set_password(password1)
                        cpuser.save()
                        msg = "重置成功"
                        return render(request,'accounts/usereditpassword.html',{'id':id,'msg':msg})
                    else:
                        msg = "重置失败,只能重置非管理员和自己的密码"
                        return render(request,'accounts/usereditpassword.html',{'id':id,'msg':msg})
                        
        else:
            #get 取出用户名，并吧用户名和id传过去
            username = cpuser.get_username() 
            return render(request,'accounts/usereditpassword.html',{'id':id,'username':username})
    else:
        return HttpResponseRedirect('/')



@login_required
def user_del(request,id):
    if request.user.is_superuser is True:
        deluser = get_object_or_404(User,pk=int(id)) 
        if deluser.is_superuser is False:
            deluser.delete()
            return HttpResponseRedirect('/accounts/user_list/')
        elif deluser.username == 'root':
            return HttpResponseRedirect('/accounts/user_list/')
        elif request.user.username == 'root':
            deluser.delete()
            return HttpResponseRedirect('/accounts/user_list/') 
        else:
            return HttpResponseRedirect('/accounts/user_list/')
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
@login_required
def user_edit_permission(request,id):
    #根据id查询出用户名
    ob = User.objects.filter(id=id).values("username")
    for o in ob:
        username = o['username']
    #如果是管理员则允许编辑权限
    if request.user.is_superuser is True:
        #提交编辑用户项目权限
        if request.method == "POST":
            #"提交编辑用户项目权限"
            poststr = ','.join(request.POST.getlist('arr'))
            from release.models import permission
            qo = permission.objects.get(username_id=username)
            qo.ownprojectid = poststr
            qo.save()
            
            msg = "权限编辑成功" 
            return HttpResponse(msg)
            #return render(request,'accounts/userpermission.html',{'msg': msg } )



        #获取用户项目权限
        if request.method == "GET":
            #通过id获取username
            o=User.objects.filter(id=id)
            for i in o:
                username = i.username
            #再通过username获取项目id列表
            from release.models import permission
            from release.models import projectinfo
            ownpid = permission.objects.filter(username_id=username)
            allprojo = projectinfo.objects.filter(isinit=1)
            uname = ""
            prostr = "" 
            for i in ownpid:
                prostr = str(i.ownprojectid).strip()
                uname = str(i.username_id)
            
            #如果从权限表中查到该用户则查出权限
            if uname:
                #项目列表不为空
                if prostr:
                    prolist = filter(None,prostr.split(','))
                    try:
                        projo = projectinfo.objects.filter(id__in=prolist).filter(isinit=1)
                    except ValueError:
                        return HttpResponseRedirect('/')
                    else:
                        #print "获得了列表"
                        #这里的allprojo是通过求差得出
                        allprojo = projectinfo.objects.filter(isinit=1).exclude(id__in=prolist)
                        return render(request,'accounts/userpermission.html',{'id':id,'username':username,'projo':projo,'allprojo': allprojo } ) 
                #项目列表为空
                else:
                    #print "项目权限列表为空"
                    return render(request,'accounts/userpermission.html',{'id':id,'username':username,'allprojo':allprojo}) 

            #如果没查到该用户则该用户写入权限表，对应项目id为空,也允许跳到编辑页面
            else:
                #没有该用户,向权限表中插入用户名
                q = permission(username_id=username)
                q.save()
                return render(request,'accounts/userpermission.html',{'id':id,'username':username,'allprojo':allprojo})
                


    #不是管理员则直接返回到首页
    else:
        return HttpResponseRedirect('/')
