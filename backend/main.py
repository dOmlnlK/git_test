


class ArgvHandler(object):
    """接收用户参数，调用相应功能"""
    def __init__(self,sys_args):
        self.sys_args = sys_args

    def help_msg(self,error_msg=""):
        """打印帮助信息"""
        msg = """
        %s
        run    启动用户交互程序
        """%error_msg


    def call(self):
        if len(self.sys_args) == 1:
            self.help_msg()

        if hasattr(self,self.sys_args[1]):
            func = getattr(self,self.sys_args[1])
            func()
        else:
            self.help_msg("没有找到该方法:%S"%self.sys_args[1])

    def run(self):
        """启动用户交互程序"""
        from backend.ssh_interactive import SSHhandler
        obj = SSHhandler(self)
        obj.interactive()
