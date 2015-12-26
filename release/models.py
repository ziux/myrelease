from django.db import models

# Create your models here.
class projectinfo(models.Model):
    name = models.CharField(max_length=200,unique=True)
    types = models.CharField(max_length=100)
    devsvnurl = models.CharField(max_length=300)
    devsvnuser = models.CharField(max_length=100)
    devsvnpasswd = models.CharField(max_length=200)
    releasesvnurl = models.CharField(max_length=300)
    releasesvnuser = models.CharField(max_length=100)
    releasesvnpasswd = models.CharField(max_length=200)
    lastretime = models.DateTimeField(max_length=200)
    isinit = models.BooleanField()
     
    def __unicode__(self):
        return self.name

class release(models.Model):
    name = models.ForeignKey(projectinfo,related_name='project_release')
    retime = models.DateTimeField(max_length=200)
    releaser = models.CharField(max_length=200) 
    restatus = models.CharField(max_length=200)
    relog = models.TextField(null=False)
    comments = models.CharField(max_length=800)
    
    def __unicode__(self):
        return self.name

