import abc
import json
from typing import Callable

from src.CoAP.constants import *


class Command(metaclass=abc.ABCMeta):

    def __init__(self,call_fct:Callable=None):
        self.call_fct=call_fct

    @staticmethod
    @abc.abstractmethod
    def get_class():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_code():
        pass

    @staticmethod
    @abc.abstractmethod
    def response_needed():
        pass


    @abc.abstractmethod
    def payload(self):
        pass

    @abc.abstractmethod
    def parse_response(self):
        pass


class detailsCommand(Command): #list files properties

    def __init__(self, pathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.pathName=pathName
        self.mType=TYPE_NON_CON_MSG  # cererea este confirmabila doar daca se solicita acest lucru din GUI



    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_GET

    @staticmethod
    def response_needed():
        return True


    def payload(self):
        p={
            "cmd":"details",
            "path":self.pathName
        }

        return json.dumps(p)

    def parse_response(self):
        pass



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

    def __init__(self, pathName: str, type: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.pathName=pathName
        self.type=type #file or folder
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return False


    def payload(self):
        p={
            "cmd":"create",
            "path":self.pathName,
            "type":self.type
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class openCommand(Command): #response is the content of file
    def __init__(self, openedPathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.openedPathName=openedPathName
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_GET

    @staticmethod
    def response_needed():
        return True

    def payload(self):
        p={
            "cmd":"open",
            "path":self.openedPathName,
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class saveCommand(Command):
    def __init__(self, savedPathName: str, savedContent: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.savedPathName=savedPathName
        self.savedContent=savedContent
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return False

    def payload(self):
        p={
            "cmd":"save",
            "path":self.savedPathName,
            "content":self.savedContent
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class deleteCommand(Command):
    def __init__(self, deletedPathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.deletedPathName=deletedPathName
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return False

    def payload(self):
        p={
            "cmd":"delete",
            "path":self.deletedPathName,
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class renameCommand(Command):
    def __init__(self, path: str, name: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.path=path
        self.name=name
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return False

    def payload(self):
        p={
            "cmd":"rename",
            "path":self.path,
            "name":self.name
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class moveCommand(Command):
    def __init__(self, sourcePath: str, destinationPath: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.sourcePath=sourcePath
        self.destinationPath=destinationPath
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return False

    def payload(self):
        p={
            "cmd":"move",
            "sourcePath":self.sourcePath,
            "destinationPath":self.destinationPath
        }

        return json.dumps(p)

    def parse_response(self):
        pass

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
    def __init__(self, currentPath: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.currentPath=currentPath
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_POST

    @staticmethod
    def response_needed():
        return True


    def payload(self):
        p={
            "cmd":"back",
            "path":self.currentPath
        }

        return json.dumps(p)

    def parse_response(self):
        pass


class searchCommand(Command):
    def __init__(self, searchedPathName: str, targetName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.searchedPathName=searchedPathName
        self.targetName=targetName
        self.mType=TYPE_NON_CON_MSG

    @staticmethod
    def get_class():
        return CLASS_METHOD

    @staticmethod
    def get_code():
        return CODE_SEARCH

    @staticmethod
    def response_needed():
        return True

    def payload(self):
        p={
            "cmd":"search",
            "path":self.searchedPathName,
            "target_name_regex":self.targetName

        }

        return json.dumps(p)

    def parse_response(self):
        pass
