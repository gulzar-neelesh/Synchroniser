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
                itemReplicaPath = self.replicaPath +'/'+str(item)
                h1 = hashlib.md5()
                with open(itemPath, 'rb') as f: # Open the file to read it's bytes
                    fb = f.read(self.block_size) # Read from the file. Take in the amount declared above
                    while len(fb) > 0: # While there is still data being read from the file
                        h1.update(fb) # Update the hash
                        fb = f.read(self.block_size) # Read the next block from the file
                sourceHash = h1.hexdigest() # Get the hexadecimal digest of the hash
                if os.path.exists(itemReplicaPath):
                    #file exists check if it needs modification
                    continue
                else:
                    #file does not exist, copy paste here
                    print('i am here')
                    shutil.copyfile(itemPath, itemReplicaPath)
                



#class Synchroniser(Digest):

#    def __init__(self, sourcePath, replicaPath) -> None:
#    super().__init__()
###

if __name__ == "__main__":
    sourceDist = input('Please enter the full path of source folder (where you will store files): ')
    replicaDist = input('Please enter the full path of replica folder (where you want all data to be replicated): ')
    a = FileManagement(str(sourceDist),str(replicaDist))
    a.checkDir('')
