import abc


class TreeItem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self,name):
        self.name=name


    @abc.abstractmethod
    def __str__(self):
        pass





class File(TreeItem):

    def __init__(self, name: str,content:str = ''):
        super().__init__(name)
        self.content=content
        self.type='file'

    def __str__(self):
        return  f"{self.type} : {self.name}"




class Directory(TreeItem):
    def __init__(self, name: str): # name = pathName
        super().__init__(name)
        self.items=[]
        self.type='directory'

    def add_item(self,item:TreeItem):
        self.items.append(item)


    def __str__(self):
        display = f"{self.type} : {self.name}"

        if len(self.items)>0:
            for item in self.items:
                display += f"\n\t  {item.type} : {item.name}"

            return display

        return None


