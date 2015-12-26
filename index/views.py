# coding=utf8
from django.shortcuts import render,get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    #首页公共部分参数：项目数，发布次数，用户总数等 
    from release.models import projectinfo
    from release.models import release
    from django.contrib.auth.models import User

    release_all_counts = release.objects.all().count()
    user_counts = User.objects.all().count()
    project_counts = projectinfo.objects.filter(isinit=1).count() 

    request.session['release_all_counts'] = release_all_counts
    request.session['user_counts'] = user_counts
    request.session['project_counts'] = project_counts

    #
    request.session['domain'] = request.META['HTTP_HOST']
    
    import django
    request.session['django_version'] = django.get_version()

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    for i in cursor.fetchone():
        request.session['mysql_version'] = i

    request.session['server_ip'] = getserverip()

    #disk
    import statvfs
    import os
    vfs = os.statvfs("/")
    available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)
    capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1024*1024*1024)

    request.session['disk_available'] = available 
    request.session['disk_capacity'] = capacity 

    return render(request,'index/index.html')

def getserverip():
    import socket
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('192.168.6.3', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

