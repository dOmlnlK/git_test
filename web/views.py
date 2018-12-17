from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import json
from backend.MultiTask import MultiTaskManager
from web import models

# Create your views here.



def acc_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            login(request,user)

            return redirect(request.GET.get("next","/"))

    return render(request,"login.html")

@login_required()
def acc_logout(request):
    logout(request)

    return redirect("/login/")

@login_required()
def index(request):

    return render(request,"index.html")


@login_required()
def web_ssh(request):

    return render(request,"web_ssh.html")


@login_required()
def batch_cmd(request):
    return render(request, 'batch_cmd.html')



@login_required()
def file_transfer(request):
    return render(request, 'file_transfer.html')


@login_required()
def batch_task_mgr(request):
    print(request.POST,"post>>")
    task_manager_obj = MultiTaskManager(request)
    print("end")


    response = {
        "task_id":task_manager_obj.task_obj.id,
        "selected_hosts_data":list(task_manager_obj.task_obj.childrentaskresult_set.all().values(
            "host2remote_user__host__ip",
            "host2remote_user__host__name",
            "id",
            "status"

        ))
    }

    return HttpResponse(json.dumps(response))



def task_result(request):
    task_id = request.GET.get("task_id")

    result = list(models.ChildrenTaskResult.objects.filter(task_id=task_id).values("id","result","status"))

    return HttpResponse(json.dumps(result))