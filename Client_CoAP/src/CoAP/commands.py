import abc
import json

from src.CoAP.constants import *


class Command(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def getClass():
        pass

    @staticmethod
    @abc.abstractmethod
    def getCode():
        pass

    @staticmethod
    @abc.abstractmethod
    def responseNeeded():
        pass

    @abc.abstractmethod
    def payload(self):
        pass


class detailsCommand(Command): #list files properties

    def __init__(self,pathName:str):
        self.pathName=pathName

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_GET

    @staticmethod
    def responseNeeded():
        return True


    def payload(self):
        p={
            "cmd":"details",
            "path":self.pathName
        }

        return json.dumps(p)



# class createDirCommand(Command):
#
#     def __init__(self,dirName:str):
#         self.dirName=dirName
#
#     @staticmethod
#     def getClass():
#         return 0
#
#     @staticmethod
#     def getCode():
#         return constants.Method.POST
#
#     @staticmethod
#     def responseNeeded():
#         return False



class createCommand(Command):

    def __init__(self,pathName:str,type:str):
        self.pathName=pathName
        self.type=type #file or folder

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return False


    def payload(self):
        p={
            "cmd":"create",
            "path":self.pathName,
            "type":self.type
        }

        return json.dumps(p)


class openCommand(Command): #response is the content of file
    def __init__(self,openedPathName:str):
        self.openedPathName=openedPathName

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return True

    def payload(self):
        p={
            "cmd":"open",
            "path":self.openedPathName,
        }

        return json.dumps(p)


class saveCommand(Command):
    def __init__(self,savedPathName:str,savedContent:str):
        self.savedPathName=savedPathName
        self.savedContent=savedContent

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return False

    def payload(self):
        p={
            "cmd":"save",
            "path":self.savedPathName,
            "content":self.savedContent
        }

        return json.dumps(p)


class deleteCommand(Command):
    def __init__(self,deletedPathName:str):
        self.deletedPathName=deletedPathName

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return False

    def payload(self):
        p={
            "cmd":"delete",
            "path":self.deletedPathName,
        }

        return json.dumps(p)


class renameCommand(Command):
    def __init__(self,path:str,name:str):
        self.path=path
        self.name=name

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return False

    def payload(self):
        p={
            "cmd":"rename",
            "path":self.path,
            "name":self.name
        }

        return json.dumps(p)


class moveCommand(Command):
    def __init__(self,sourcePath:str,destinationPath:str):
        self.sourcePath=sourcePath
        self.destinationPath=destinationPath


    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return False

    def payload(self):
        p={
            "cmd":"move",
            "sourcePath":self.sourcePath,
            "destinationPath":self.destinationPath
        }

        return json.dumps(p)

#
# class cdCommand(Command):
#     def __init__(self,newPathName:str):
#         self.newPathName=newPathName
#
#     @staticmethod
#     def getClass():
#         return 0
#
#     @staticmethod
#     def getCode():
#         return constants.Method.POST
#
#     @staticmethod
#     def responseNeeded():
#         return True

class backCommand(Command):
    def __init__(self,currentPath:str):
        self.currentPath=currentPath

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_POST

    @staticmethod
    def responseNeeded():
        return True


    def payload(self):
        p={
            "cmd":"back",
            "path":self.currentPath
        }

        return json.dumps(p)


class searchCommand(Command):
    def __init__(self,searchedPathName:str,targetName:str):
        self.searchedPathName=searchedPathName
        self.targetName=targetName

    @staticmethod
    def getClass():
        return CLASS_METHOD

    @staticmethod
    def getCode():
        return CODE_SEARCH

    @staticmethod
    def responseNeeded():
        return True

    def payload(self):
        p={
            "cmd":"search",
            "path":self.searchedPathName,
            "target_name_regex":self.targetName

        }

        return json.dumps(p)
