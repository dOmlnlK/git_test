import sys, os, json
import time, socket
from concurrent.futures import ThreadPoolExecutor

import paramiko


def ssh_cmd(sub_task_obj):
    host2remote_user_obj = sub_task_obj.host2remote_user

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host2remote_user_obj.host.ip,
                    port=host2remote_user_obj.host.port,
                    username=host2remote_user_obj.remote_user.username,
                    password=host2remote_user_obj.remote_user.password,
                    timeout=5)
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.content)
        stdout_ret = stdout.read()
        stderr_ret = stderr.read()

        # task_log_obj = models.TaskLogDetail.objects.get(task=task_obj,host_to_remote_user_id=host_to_user_obj.id)
        sub_task_obj.result = stdout_ret + stderr_ret
        print("------------result-------------")
        print(sub_task_obj.result)

        if stderr_ret:
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 1
    except Exception as e:
        sub_task_obj.result = e
        sub_task_obj.status = 2

    sub_task_obj.save()

    ssh.close()


def file_transfer(sub_task_obj, task_data):
    host2remote_user_obj = sub_task_obj.host2remote_user
    file_transfer_type = task_data["file_transfer_type"]

    remote_file_path = task_data.get("remote_file_path")

    try:
        t = paramiko.Transport((host2remote_user_obj.host.ip, host2remote_user_obj.host.port))
        t.connect(username=host2remote_user_obj.remote_user.username,
                  password=host2remote_user_obj.remote_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if file_transfer_type == "send":
            local_file_path = task_data.get("local_file_path")
            sftp.put(local_file_path,remote_file_path)
            result = "upload local file [%s] succeed!" % local_file_path
        else:
            local_file_path = conf.settings.DOWNLOAD_DIR
            if not os.path.isdir("%s/%s" % (local_file_path, task_obj.id)):
                os.mkdir("%s/%s" % (local_file_path, task_obj.id))

            filename = "[%s]%s" % (host2remote_user_obj.host.ip,  remote_file_path.split('/')[-1])
            sftp.get(remote_file_path, "%s/%s/%s" % (local_file_path, sub_task_obj.task.id, filename))
            result = "download remote file [%s] succeed!" % remote_file_path

        sub_task_obj.status = 1
        sub_task_obj.result = result
        t.close()


    except Exception as e:
        sub_task_obj.status = 2
        sub_task_obj.result = e

    sub_task_obj.save()




if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myFortress.settings")
    import django

    django.setup()
    from django import conf
    from web import models

    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)
    print("task runner..", task_obj)

    pool = ThreadPoolExecutor(10)

    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.childrentaskresult_set.all():
            pool.submit(ssh_cmd, sub_task_obj)
    else:
        task_data = json.loads(task_obj.content)
        for sub_task_obj in task_obj.childrentaskresult_set.all():
            pool.submit(file_transfer, sub_task_obj, task_data)
    pool.shutdown(wait=True)
