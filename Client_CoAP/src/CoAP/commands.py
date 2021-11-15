import abc
import constants

class Command(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    @staticmethod
    def getClass():
        pass

    @abc.abstractmethod
    @staticmethod
    def getCode():
        pass

    @abc.abstractmethod
    @staticmethod
    def responseNeeded():
        pass


class lsCommand(Command):

    def __init__(self,dirName:str):
        self.dirName=dirName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.GET

    @staticmethod
    def responseNeeded():
        return True




class createDirCommand(Command):

    def __init__(self,dirName:str):
        self.dirName=dirName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False



class createFileCommand(Command):

    def __init__(self,fileName:str):
        self.dirName=fileName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False

class openCommand(Command):
    def __init__(self,openedFileName:str):
        self.openedFileName=openedFileName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return True


class saveCommand(Command):
    def __init__(self,savedFileName:str,pathForSaving:str,savedContent:str):
        self.savedFileName=savedFileName
        self.pathForSaving=pathForSaving
        self.savedContent=savedContent

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False

class DeleteCommand(Command):
    def __init__(self,deletedFileName:str):
        self.deletedFileName=deletedFileName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False



class renameCommand(Command):
    def __init__(self,newFileName:str):
        self.newFileName=newFileName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False


class moveCommand(Command):
    def __init__(self,newPathName:str):
        self.newPathName=newPathName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return False


class cdCommand(Command):
    def __init__(self,newPathName:str):
        self.newPathName=newPathName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return True

class dirBackCommand(Command):

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.POST

    @staticmethod
    def responseNeeded():
        return True

class searchCommand(Command):
    def __init__(self,searchedPathName:str):
        self.searchedPathName=searchedPathName

    @staticmethod
    def getClass():
        return 0

    @staticmethod
    def getCode():
        return constants.Method.SEARCH

    @staticmethod
    def responseNeeded():
        return True

