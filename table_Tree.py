#coding=utf-8
from Graph_Node import Graph_Node
from Table_And_Task_List import All_table_task
class Task_Tree(object):
    def Table_List(self,table_relation_list):
        #定义所有表list
        table_list=[]
        tree_node_list=[]
        for i in table_relation_list:
            for j in range(len(i)):
                table_list.append(i[j])
        table_list=list(set(table_list))

        for x in range(len(table_list)):
            tree_node_list.append([])


        for y in range(len(tree_node_list)):
            tree_node_list[y]=Graph_Node()
            tree_node_list[y].val=table_list[y]
            parents=[]
            childs=[]
            for z in table_relation_list:
                if z[0]==tree_node_list[y].val:
                    parents.append(z[1])
                if z[1]==tree_node_list[y].val:
                    childs.append(z[0])
            tree_node_list[y].parents=parents
            tree_node_list[y].childs=childs
            print     "%s:parents:%s,childs:%s\n\n"%(tree_node_list[y].val,tree_node_list[y].parents,tree_node_list[y].childs)

        return tree_node_list


a=All_table_task()
s=a.all_table_task("wish_indus")
b=Task_Tree()
b.Table_List(s[1])
c= b.Table_List(s[1])























