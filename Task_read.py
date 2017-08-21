#coding=utf-8

import os
import os.path
class Task_Read(object):
    #获得目录下所有任务名以及路径
    def get_taskname(self,filepath):
        rootdir=filepath
        path=[]
        filenames_list=[]
        for parent,dirnames,filenames in os.walk(rootdir):
            for filename in filenames:
                filenames_list.append(filename)
                path.append(os.path.join(parent,filename))
        return filenames_list,path

    #获得任务脚本内容
    def get_script(self,path):
        with open(path,'r') as f:
            return (f.read())




    #print "task_relation_list:",all_task[i].reliability[0],"\ntable_relation_list:",all_task[i].reliability[1]










#table_Task1=Task_Read()
#print table_Task1.get_taskname("./File")
#print table_Task1.get_script("./File/st_shopee_item_rate_milestone")