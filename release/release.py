# coding=utf8
import os
import commands
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def release(comments,reobj,username):
    #执行同步和提交svn等预发布动作
    #1.更新svn到本地目录(判断本地svn目录是否存在，存在则更新代码，初始化这里暂不考虑)
    name = reobj.name
    times = time.strftime('%Y-%m-%d %H:%M:%S')
    basedirectory = '/data/release/'
    svndirectory = basedirectory+reobj.name+'/trunk/'
    resvndirectory = basedirectory+reobj.name+ '/release/'
    excludefile = basedirectory+reobj.name+'/'+'exclude.list'
    svnupcmd = 'svn up '+ svndirectory
    (svnupexitstatus, svnupouttext) = commands.getstatusoutput(svnupcmd)

    #2.同步到发布目录(判断发布目录是否存在，存在则执行同步)
    rint = 0
    rsynccmd = 'rsync  -vzrtopg --delete --progress --exclude-from='+excludefile+ ' '+ svndirectory + ' '+resvndirectory
    (rsyncexitstatus, rsyncouttext) = commands.getstatusoutput(rsynccmd)
    rint = rint + rsyncexitstatus

    if int(rsyncexitstatus) != 0:
        result = "同步有问题,请检查目录"
        return result
    #3.进入发布目录 提交到发布svn(进入发布目录提交代码，如果有新增代码还需要新增。另外提交代码需要注释，初始化暂不考虑)
    #进入目录 并查询是否有新文件
    #检查是否目录是否下有变化的文件数量
    cdcacmd = 'cd '+resvndirectory+';svn st | wc -l'
    (cdcaexitstatus, cdcaouttext) = commands.getstatusoutput(cdcacmd)
    if int(cdcaouttext) > 0:
    
         #检查发布svn目录下是否有需要提交的文件数量
        
        cdccmd = 'cd '+resvndirectory+';svn st  | awk \'{if ( $1 == "?") { print $0}}\' | wc -l'
        (cdcexitstatus, cdcouttext) = commands.getstatusoutput(cdccmd)
        #如果有新增的文件 怎准备循环添加
        aint = 0
        if int(cdcouttext) > 0:
            cdcfilecmd = 'cd '+resvndirectory+';svn st |awk \'{if ( $1 == "?") { print $0}}\' | cut -nb 9- '
            (cdcfileexitstatus, cdcfileouttext) = commands.getstatusoutput(cdcfilecmd)
            for line in cdcfileouttext.split("\n"):
                line = '"' + line +'"'
                cdacmd = 'cd '+resvndirectory+';svn add '+line
                (cdaexitstatus, cdaouttext) = commands.getstatusoutput(cdacmd)
                aint = aint + cdaexitstatus
    
        #检查发布svn目录下是否有需要删除的文件数量
        cdcdcmd = 'cd '+resvndirectory+';svn st  | awk \'{if ( $1 == "!") { print $0}}\' | wc -l'
        (cdcdexitstatus, cdcdouttext) = commands.getstatusoutput(cdcdcmd)
        #如果有需要删除的文件 怎准备循环删除
        dint = 0
        if int(cdcdouttext) > 0:
            cdcdfilecmd = 'cd '+resvndirectory+';svn st |awk \'{if ( $1 == "!") { print $0}}\' | cut -nb 9- '
            (cdcdfileexitstatus, cdcdfileouttext) = commands.getstatusoutput(cdcdfilecmd)
            for line in cdcdfileouttext.split("\n"):
                line = '"' + line +'"'
                cddcmd = 'cd '+resvndirectory+';svn rm '+line
                (cddexitstatus, cddouttext) = commands.getstatusoutput(cddcmd)
                dint = dint+cddexitstatus
        #最后提交svn
        comments = '\'' + comments +'\''
        cdcommitcmd = 'cd '+resvndirectory+';svn commit -m '+ comments
        (cdcommitexitstatus, cdcommitouttext) = commands.getstatusoutput(cdcommitcmd)
        svnuprecmd = 'cd '+resvndirectory+';svn up '
        (svnupreexitstatus, svnupreouttext) = commands.getstatusoutput(svnuprecmd)
        if int(cdcommitexitstatus) + dint + aint  + rint == 0:
            result = "发布成功"
        else :
            result = "发布异常"

        #不管发布成功和失败，这里需要写入日志
        reobj.lastretime = times
        reobj.save() 
        #写入预发布日志到数据库
          
        logs(reobj,result,times,comments,svnupcmd,svnupouttext,rsynccmd,rsyncouttext,cdcommitcmd,cdcommitouttext,username)
        #写入发布记录列表到数据库,其中把发布时间写入到
        
    else:
        #这里没有发布内容则不写入日志，前台提示没有发布内容即可
        #这里后期可以写系统操作日志
        result = "没有需要发布的内容"
    return result 


def mkDir(path):
    if os.path.exists(path) is False:
        os.makedirs(path)
    pass


def logs(reobj,result,times,comments,svnupcmd,svnupouttext,rsynccmd,rsyncouttext,cdcommitcmd,cdcommitouttext,username):
    with open(os.getcwd()+'/release/log.tpl') as file:
        logtpl = file.read()
    log =  logtpl % {'name': reobj.name,'result': result,'times': times,'comments': comments,'svnupcmd': svnupcmd,'svnupouttext': svnupouttext,'rsynccmd':rsynccmd,'rsyncouttext':rsyncouttext,'cdcommitcmd':cdcommitcmd,'cdcommitouttext':cdcommitouttext,'username':username}
    from .models import release
    r = release(name=reobj,retime=times,releaser=username,restatus=result,relog=log,comments=comments)
    r.save()
    
    
