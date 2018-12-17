from django.contrib import admin
from web import models

class ChildTaskAdmin(admin.ModelAdmin):
    list_display = ["id","status","task",]

class TaskAdmin(admin.ModelAdmin):
    list_display = ["id","task_type","content","date"]



# Register your models here.

admin.site.register(models.Host)
admin.site.register(models.HostCroup)
admin.site.register(models.Host2RemoteUser)
admin.site.register(models.UserInfo)
admin.site.register(models.RemoteUser)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.ChildrenTaskResult,ChildTaskAdmin)

