#coding=utf-8
from ParseTable import Parse_Table
from Task  import *
from Task_Read import Task_Read
class All_table_task(object):
    def all_table_task(self,roodir):
        Table_task=Task_Read()
        Parse_table=Parse_Table()
        #获得指定文件夹下所有任务
        task_name_list=Table_task.get_taskname(roodir)
        all_task=[]#定义all_task用来存task对象
        tmp_task_relation_list=[]#定义tmp_task_relation_list临时用来存所有output表以及对应任务关系
        tmp_table_relation_list=[]#定义tmp_table_relation_list临时用来存所有表对应任务关系
        task_relation_list=[]#输出表与任务关系
        table_relation_list=[]#输出表与输入表任务关系

        #获得一个和任务量相同长度的list，用来存所有task对象
        for i in range(len(task_name_list[1])):
            all_task.append([])

        #存所有任务的依赖
        for i in range(len(all_task)):
            all_task[i]=Task(task_name_list[0][i],"hive_task")
            all_task[i].script=Table_task.get_script(task_name_list[1][i])
            table_list=Parse_table.extract_table_name(all_task[i].script)
            all_task[i].reliability=Parse_table.create_relation_list(table_list[0],table_list[1],all_task[i].taskname)
            tmp_task_relation_list.append(all_task[i].reliability[0])
            tmp_table_relation_list.append(all_task[i].reliability[1])

        #将每个二维嵌套数组拆开
        for i in tmp_task_relation_list:
            for j in range(len(i)):
                task_relation_list.append(i[j])
        #同上
        for x in tmp_table_relation_list:
            for y in range(len(x)):
                table_relation_list.append(x[y])
        #task_relation_list：（output表名,task名字），table_relation_list：（output表名，input表名）
        return task_relation_list,table_relation_list


a=All_table_task()
s=a.all_table_task("File")
#import csv
#with open("zz.csv","w") as f:
#    for line in s[1]:
#        f.write(",".join(line)+"\n")
#
#
#print s[1]
#

