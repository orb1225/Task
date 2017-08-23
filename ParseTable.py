#coding=utf-8
import re

class Parse_Table(object):
    #解析出表名，作为依赖任务名称
    def extract_table_name(self,script):
        text=script
        #找出from后面第一个符合条件的值，也就是表名
        #input_table_set=set(re.findall("from\s+([\w|\.|\,]+)?",text))
        input_table_set=set(re.findall("(?<=from|join)\s+([\w\.\,]+)?",text))
        #找出insert overwrite table后面的表名
        output_table_set=set(re.findall("insert\s+overwrite\s+table\s+([\w\.\,]+)?",text))
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
b="""alter table st_wish_shop_cat_fatdt30 drop partition(pt=${pt});
insert overwrite table st_wish_sho|p_cat_fatdt30 partition(pt=${pt})
select "${dt}" insert_date,merchant_id,acat_id,sum(amount_30),sum(price_30),sum(wish_save_30),sum(rate_num_30),
count(*) item_count,count(if(amount_30>0,1,NULL)) hot_item_count,count(if(already_recommended_flag=1,1,NULL)) wish_recommended_count,
sum(seller_price+seller_freight_price)/count(*) avg_price,
coalesce(sum(if(amount_30>0,seller_price+seller_freight_price,0))/count(if(amount_30>0,1,NULL)),0) hot_avg_price
from (
select a.cat_id acat_id,b.*,Row_Number() OVER (partition by a.cat_id,b.merchant_id,b.itemid ORDER BY b.amount_1 desc) sort_order
from (select * from dw_wish_tmp_cat_dimt0 where pt=${g_wish_cat_pt}) a
inner join (select *
            from st_wish_item_base_fatdt0 lateral view explode(split(cat_ids,"\;")) subview AS cat_id
            where pt=${pt} and removed_flag=0 and deleted_flag=0) b on(a.sub_id=b.cat_id)
) x
where sort_order=1
group by merchant_id,acat_id;"""
s=a.extract_table_name(b)
#print s[0],s[1]
d=a.create_relation_list(s[0],s[1],"st_shopee_item_milestone_fatdt0")
#print d


