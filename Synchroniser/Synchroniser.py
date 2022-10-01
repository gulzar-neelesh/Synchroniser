from ast import Str
import hashlib
import sched, time
import os


class Digest:
    
    def readFileContent(filePath) -> Str:
        #use the file path to get the file
        return fileData

    
    def getDigest(fileData):
        return fileDigest

class FileManagement():

    def __init__(self, sourcePath, replicaPath) -> None:
        self.completedDirList = []
        self.sourcePath = sourcePath
        self.iterationPath = ''
        self.replicaPath = replicaPath

    def checkDir(self, newPath)  -> None:
        if newPath == '':
            itemsList = os.listdir(self.sourcePath)
        else:
            itemsList = os.listdir(self.iterationPath)

        for item in itemsList:
            itemPath = self.sourcePath + '/' + str(item)
            if os.path.isdir(itemPath) == True:
                self.iterationPath = itemPath
                self.checkDir(itemPath)



#class Synchroniser(Digest):

#    def __init__(self, sourcePath, replicaPath) -> None:
#    super().__init__()
###

if __name__ == "__main__":
    curDir = os.getcwd()
    completedDirList=[]
    itemList = os.listdir(curDir+"/source")

    for item in itemList:
        itemPath = str(curDir) + "/source/" + str(item)
        print(itemPath)
        if os.path.isdir(itemPath) == True:
            ##call the same function again recusion till all you have is files in each dir
            print ("I am in a directory and I will keep digging deeper")
        if os.path.isfile(itemPath) == True:
            print("I am in a file and I should copy this to replica")

            


    text1 = b"this is my home"
    text2 = b"this is my home"

    h1 = hashlib.md5()
    h2 = hashlib.md5()

    h1.update(text1)
    h2.update(text2)

    print(h1.hexdigest() == h2.hexdigest())

    #print(curDir)