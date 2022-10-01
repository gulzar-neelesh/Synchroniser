from ast import Str
import hashlib
import sched, time
import shutil
import os

class FileManagement():

    def __init__(self, sourcePath, replicaPath) -> None:
        self.completedOuterDirList = []
        self.sourcePath = sourcePath
        self.iterationPath = ''
        self.replicaPath = replicaPath
        self.block_size = 65536

    def checkDir(self, newPath)  -> None:
        if newPath == '':
            itemsList = os.listdir(self.sourcePath)
        else:
            itemsList = os.listdir(self.iterationPath)

        for item in itemsList:
            itemPath = self.sourcePath + '/' + str(item)
            if os.path.isdir(itemPath) == True:
                self.iterationPath = itemPath
                self.completedOuterDirList.append(self.iterationPath)
            else:
                # the it is some sort of file in that directory
                h1 = hashlib.md5()
                with open(itemPath, 'rb') as f: # Open the file to read it's bytes
                    fb = f.read(self.block_size) # Read from the file. Take in the amount declared above
                    while len(fb) > 0: # While there is still data being read from the file
                        h1.update(fb) # Update the hash
                        fb = f.read(self.block_size) # Read the next block from the file
                sourceHash = file_hash.hexdigest() # Get the hexadecimal digest of the hash
                if os.path.exists(itemPath):
                    #file exists check if it needs modification
                    continue
                else:
                    #file does not exist, copy paste here
                    itemReplicaPath = self.replicaPath +'/'+str(item)
                    shutil.copyfile(itemPath, itemReplicaPath)
                



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