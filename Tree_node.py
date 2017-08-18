class Tree_node(object):
    def __init__(self,**kwargs):
        self.val = kwargs.get("val","")
        self.parents=kwargs.get("parents",[])
        self.sons=kwargs.get("sons",[])
