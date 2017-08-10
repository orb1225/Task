import time
class Task(object):
    def __init__(self,taskname,type,*args):
    #初始化：任务名，任务类型，创建时间，执行状态（0：未执行，1：执行完成，2：正在执行，3：错误），优先级（越大越优先）
        self.create_time = time.strftime("%Y%m%d")
        self.status = 0
        self.priority=3
        self.taskname=taskname
        self.type=type#hive任务或者同步任务
        self.create_time,self.status,self.priority=args


a=Task('a','hive')
print a.priority