import json
from web import models
import subprocess
from django import conf



class MultiTaskManager(object):
    def __init__(self,request):
        self.request = request
        self.task_run()


    def task_parser(self):      #task_data {'selected_hosts': ['1', '2', '4', '4', '5', '5'], 'cmd': 'df', 'task_type': 'cmd'}
        """任务解析"""
        self.task_data = json.loads(self.request.POST.get('task_data'))
        task_type = self.task_data.get("task_type")

        if task_type:
            task_func = getattr(self,task_type)
            task_func()

        else:
            print("cannot find task",task_type)



    def task_run(self):
        """任务执行"""
        self.task_parser()

    def cmd(self):
        """
        命令类型任务
        1. 生成任务在数据库中的记录,拿到任务id
        2.触发任务, 不阻塞
        3.返回任务id给前端
        """
        task_obj = models.Task.objects.create(
            task_type = 'cmd',
            content = self.task_data.get('cmd'),
            user = self.request.user
        )

        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs =[]
        for id in selected_host_ids:
            task_log_objs.append(
                models.ChildrenTaskResult(task=task_obj,host2remote_user_id=id,result='init...')
            )
        models.ChildrenTaskResult.objects.bulk_create(task_log_objs)


        print("running batch commands....")

        task_script = "python3 %s/backend/task_runner.py %s" % (conf.settings.BASE_DIR, task_obj.id)

        cmd_process = subprocess.Popen(task_script, shell=True)

        self.task_obj = task_obj


    def file_transfer(self):

        task_obj = models.Task.objects.create(
            task_type='file_transfer',
            content=json.dumps(self.task_data),
            user=self.request.user
        )

        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(
                models.ChildrenTaskResult(task=task_obj, host2remote_user_id=id, result='init...')
            )
        models.ChildrenTaskResult.objects.bulk_create(task_log_objs)

        print("running batch commands....")

        task_script = "python3 %s/backend/task_runner.py %s" % (conf.settings.BASE_DIR, task_obj.id)

        cmd_process = subprocess.Popen(task_script, shell=True)

        self.task_obj = task_obj






