#coding=utf-8
import re

class parse_table(object):
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

    #创建任务字典
    def create_task_dict(self,input_table,output_table,taskname):#传入任务list
        input=input_table
        #判断输出表是否只有一个
        if len(output_table)>1:
            output=list(taskname)
        else:
            output=output_table
        for i in range(len(input)-1):
            output.append(output[0])
        table_dict=zip(output,input)
        return table_dict














a=parse_table()
b="""alter table st_wish_recommend_tag_pref_total_fatdt0 drop partition(pt=${pt});
insert overwrite table st_wish_recommend_tag_pref_total_fatdt0 partition(pt=${pt})
select "${dt}",a.split_item_name,count(*) as item_cnt,b.recommend_tag from
(select itemid,lower(split_item_name) as split_item_name from st_wish_itemname_detail_fatdt0 where pt=${pt}) a
inner join
(select itemid,recommend_tag from st_wish_recommend_tag_detail_fatdt0 where pt=${pt} and amount_30>0 and recommend_tag!="") b
on (a.itemid=b.itemid)
group by a.split_item_name,b.recommend_tag;

insert overwrite table st_wish_recommend_tag_pref_total_fatdt0 partition(pt=${pt})
select "${dt}",a.split_item_name,a.cnt,a.recommend_tag from
(select *,Row_Number() OVER (partition by recommend_tag order by cnt desc ) as sort
 from st_wish_recommend_tag_pref_total_fatdt0 where pt=${pt}
) a where  a.sort<=100 and length(a.split_item_name)>1 and length(a.split_item_name)<100;"""
s=a.extract_table_name(b)
d=a.create_task_dict(s[0],s[1],"a")

