from web import models
from django.contrib.auth import authenticate
from backend import paramiko_ssh




class SSHhandler(object):
    """堡垒机交互脚本"""

    def __init__(self,argv_handler_instance):
        self.argv_handler_instance = argv_handler_instance
        self.models = models

    def auth(self):
        """用户认证"""
        count = 0
        while count < 3:
            username = input("请输入堡垒机账号：").strip()
            password = input("请输入密码：").strip()
            user = authenticate(username=username,password=password)

            if user:
                self.user = user
                return True
            else:
                count += 1

    def interactive(self):
        """启动用户交互脚本"""
        if self.auth():
            print("<准备列出该用户可操作的主机组列表>")
            print(self.user.host_groups.all())
            while True:
                host_group_list = self.user.host_groups.all()
                for index,host_group_obj in enumerate(host_group_list):
                    print("%s.\t%s[%s]"%(index,host_group_obj,host_group_obj.host2remote_users.count()))

                print("z.\t未分组[%s]"%(self.user.host2remote_users.count()))

                choice = input("请输入选择主机组序号：")

                if choice.isdigit():
                    choice = int(choice)
                    selected_host_group_obj = host_group_list[choice]

                elif choice == "z":
                    selected_host_group_obj = self.user


                while True:

                        for index,host2remote_users_obj in enumerate(selected_host_group_obj.host2remote_users.all()):
                            print("%s.\t%s" % (index, host2remote_users_obj))

                        choice = input("请输入选择主机序号：").strip()

                        if choice.isdigit():
                            choice = int(choice)
                            selected_host2user_obj = selected_host_group_obj.host2remote_users.all()[choice]
                            print("going to login  %s" % selected_host2user_obj)
                            paramiko_ssh.ssh_connect(self, selected_host2user_obj)


                        if choice == "b":
                            break








