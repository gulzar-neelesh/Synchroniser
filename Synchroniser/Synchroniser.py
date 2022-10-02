import logging
import hashlib
import sched, time
import shutil
import os
import copy
from typing import List
import re

class HashDigest(): # could easily add a new hasing method with out effecting the logic
    
    def __init__(self, filePath, blockSize=65536) -> None: #65kb block size set. Increase for large files but affects the memory
        self.filePath = filePath
        self.block_size = blockSize

    def generateMD5Hash(self) -> str:
         h1 = hashlib.md5()
         with open(self.filePath, 'rb') as f: # Open the file to read it's bytes
             fb = f.read(self.block_size) # Read from the file. Take in the amount declared above
             while len(fb) > 0: # While there is still data being read from the file
                 h1.update(fb) # Update the hash
                 fb = f.read(self.block_size) # Read the next block from the file
         fileHash = h1.hexdigest() # Get the hexadecimal digest of the hash
         return fileHash

class StartUp():

    def __init__(self) -> None:
        self.freq = ''
        self.sourcePath = ''
        self.replicaPath = ''
        self.logPath = ''
    
    def getFreq(self) -> int:
        return self.freq

    def setFreq(self, freq) -> None:
        assert (type(freq)==int and freq>0), 'Frequency must be a postive integer'

    def getSourcePath(self) -> str:
        return self.sourcePath

    def getreplicaPath(self) -> str:
        return self.replicaPath

    def getlogPath(self) -> str:
        return self.logPath

class SourceToReplicaManagement():

    def __init__(self, freq, sourcePath, replicaPath) -> None:
        self.freq = freq
        self.globaDirList = []
        self.localDirList = []
        self.sourcePath = sourcePath
        self.newPath = ''
        self.iterationPath = ''
        self.pathToUseSource = ''
        self.replicaPath = replicaPath
        self.level = 0

    def fileLevelModification(self, item, itemPath) -> None:
        # the it is some sort of file in that directory
                itemReplicaPath = os.path.join(self.replicaPath, str(item))
                sourceFileHash = HashDigest(itemPath).generateMD5Hash()

                if os.path.exists(itemReplicaPath):
                    #file exists check if it needs modification
                    replicaFileHash = HashDigest(itemReplicaPath).generateMD5Hash()
                    if sourceFileHash != replicaFileHash:
                        shutil.copyfile(itemPath, itemReplicaPath) # duplicated needs to be updated                  
                else:
                    #file does not exist, copy paste here
                    print('i am here')
                    logging.info('File duplicated \n')
                    shutil.copyfile(itemPath, itemReplicaPath)

    def checkSource(self)  -> None:
        print('just ran again')
        if self.newPath == '': # very unstable way doing this check, but works
            self.pathToUseSource = self.sourcePath
        else:
            self.pathToUseSource = self.iterationPath
        
        itemsList = os.listdir(self.pathToUseSource)
        itemsList = self.ignoreTempFiles(itemsList)

        for item in itemsList:
            itemPath = os.path.join(self.pathToUseSource, str(item))
            if os.path.isdir(itemPath) == True:
                # not a file but a directory
                self.iterationPath = itemPath
                self.localDirList.append(self.iterationPath)
            else:
                # a file
                self.fileLevelModification(item, itemPath)
        self.globaDirList.append(copy.deepcopy(self.localDirList))
        self.localDirList.clear()
        self.beginBFSSearch()
        s.enter(self.freq, 1, self.checkSource)
     
    def beginBFSSearch(self)->None:
        for thisDir in self.globaDirList[self.level]:
            dirExtension = ''
            if str(thisDir).startswith(self.sourcePath):
                dirExtension = thisDir[len(self.sourcePath)+1:]
            lReplicaPath = os.path.join(self.replicaPath, thisDir)
            if os.path.exists(lReplicaPath):
                # the directory exists check file status and add dir to localDirList
                pass
            else:
                #the directory does not exists. create directory and copy all the contents into it
                pass

    
    def ignoreTempFiles(self, itemsList)->List:
        for item in itemsList:
                if item.startswith('~$'):
                    itemsList.remove(item)
        return itemsList

    def removalProcedure(self)->None:
        # start from replica and see what is different in source
        2+2
                
if __name__ == "__main__":
    
    sourceDist = input('Enter full path of source folder, where you will store files: \n')
    replicaDist = input('Enter full path of replica folder, where you want all data to be replicated: \n')
    freqs = input('Enter the frequency of periodic check (units: seconds): \n')
    freq = int(freqs)

    logging.basicConfig(filename='Logs.log', encoding='utf-8', level=logging.DEBUG)
    s=sched.scheduler(time.time, time.sleep)
  
    s.enter(freq, 1, SourceToReplicaManagement(freq, sourceDist, replicaDist).checkSource)
    s.run()
