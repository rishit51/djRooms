from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver 
from .validators import *
def category_icon_upload_path(instance,filename):
    return f"category/{instance.id}/category_icon/{filename}"
def server_icon_upload_path(instance,filename):
    return f"server/{instance.id}/server_icon/{filename}"
def server_banner_upload_path(instance,filename):
        return f"server/{instance.id}/server_banner/{filename}"

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    icon=models.FileField(upload_to=server_icon_upload_path,null=True,blank=True)
    

    def save(self,*args,**kwargs):
        if self.id:
            exisiting=get_object_or_404(Category,id=self.id)
            if exisiting.icon!=self.icon:
                exisiting.icon.delete(save=False)
        super(Category,self).save(*args,**kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def _category_delete_receiver(sender,instance, **kwargs):
        for field in instance._meta.fields:
            if field.name=="icon":
                file =getattr(instance,field.name)
                file.delete(save =False)

        
    



    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
    

class Server(models.Model):
    name=models.CharField(max_length=100)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='server_owner',null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="server_category")
    description=models.CharField(max_length=250,blank=True,null=True)
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    banner=models.ImageField(upload_to=server_banner_upload_path,null=True,blank=True)
    icon=models.ImageField(upload_to=server_icon_upload_path,null=True,blank=True,validators=[validate_icon_image])

    def save(self,*args,**kwargs):
        if self.id:
            exisiting=get_object_or_404(Category,id=self.id)
            if exisiting.icon!=self.icon:
                exisiting.icon.delete(save=False)
            if exisiting.banner!=self.banner:
                exisiting.banner.delete(save=False)
        super(Category,self).save(*args,**kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def _category_delete_receiver(sender,instance, **kwargs):
        for field in instance._meta.fields:
            if field.name=="icon" or file.name=="banner":
                file =getattr(instance,field.name)
                file.delete(save =False)

    def __str__(self):
        return self.name
class Channel(models.Model):
    name=models.CharField(max_length=100)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='channel_owner',null=True)
    topic=models.CharField(max_length=100,null=True,blank=True)
    server=models.ForeignKey(Server,on_delete=models.CASCADE,related_name="channel_server")
    def save(self,*args, **kwargs):
        self.name=self.name.lower()
        super(Channel,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name