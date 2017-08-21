#coding=utf-8
import re

class Parse_Table(object):
    #解析出表名，作为依赖任务名称
    def extract_table_name(self,script):
        text=script
        #找出from后面第一个符合条件的值，也就是表名
        input_table_set=set(re.findall("from\s+([\w|\.|\,]+)?",text))
        #找出insert overwrite table后面的表名
        output_table_set=set(re.findall("insert\s+overwrite\s+table\s+([\w|\.|\,]+)?",text))
        #去除set中的空值
        input_table_set.discard("")
        output_table_set.discard("")
        #找出输出表输入表中的交集
        ret_list=list((input_table_set.union(output_table_set))^(input_table_set^output_table_set))
       #去除输入表中和输出表值一样的表
        for i in range(len(ret_list)):
            input_table_set.discard(ret_list[i])
        #将set转成list
        input_table=list(input_table_set)
        output_table=list(output_table_set)
        return input_table,output_table

    #创建表依赖，以及输出表与任务名依赖
    def create_relation_list(self,input_table,output_table,taskname):#传入任务list
        input=input_table
        output=output_table
        #将输出表和task任务建立依赖关系：
        task_list=[taskname]
        for i in range(len(output)-1):
            task_list.append(task_list[0])
        #print "task_list:",task_list
        task_relation_list=zip(task_list,output)
        #print "task_relation_list:",task_relation_list
        table_relation_list=[]
        #将输出表与输入表建立依赖关系：
        for i in range(len(output)):
            for j in range(len(input)):
                tmp_list=[output[i],input[j]]
                table_relation_list.append(tmp_list)
        #print "table_relation_list:",table_relation_list
        return task_relation_list,table_relation_list

        #else:
         #   output=output_table
        #for i in range(len(input)-1):
        #    output.append(output[0])
        #task_dict=zip(output,input)
        #return task_dict
















#测试的，没什么用

a=Parse_Table()
b="""from
(select *
from
dw_shopee_item_dimt0  where pt=${pt}) a
inner join
(select * from dw_shopee_item_dimt0  where pt=${pt,day:1}) b
on(a.itemid=b.itemid)
insert overwrite table st_shopee_item_shopee_verified_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,
if(a.shopee_verified=0 and b.shopee_verified=1,1,0) as shopee_verified_add,
if(a.shopee_verified=1 and b.shopee_verified=0,1,0) as shopee_verified_cancel
where a.shopee_verified<>b.shopee_verified
insert overwrite table st_shopee_item_status_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,
if(a.status="" and b.status="0",1,0) as item_forbbiden,
if(a.status="" and b.status="1",1,0) as item_deleted
where a.status<>b.status and a.status=""
insert overwrite table st_shopee_item_stock_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,
a.stock  as old_stock,
b.stock  as new_stock
where a.stock<>b.stock
insert overwrite table st_shopee_item_tag_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,
a.hashtag_list ,
b.hashtag_list
where a.hashtag_list<>b.hashtag_list and a.status="" and b.status=""
insert overwrite table st_shopee_item_like_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,b.liked_count
where a.liked_count=0 and b.liked_count>0
insert overwrite table st_shopee_item_sold_month_milestone_fatdt0 partition(pt=${pt})
select "${dt}" insert_date,a.shopid,a.itemid,b.sold
where a.sold=0 and b.sold>0;"""
s=a.extract_table_name(b)
#print s[0],s[1]
d=a.create_relation_list(s[0],s[1],"st_shopee_item_milestone_fatdt0")
#print d


