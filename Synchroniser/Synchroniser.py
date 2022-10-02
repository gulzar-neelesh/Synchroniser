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
        self.globaDirList = [] # rest in the end
        self.localDirList = [] # reset in the end
        self.sourcePath = sourcePath
        self.newPath = '' # reset in the end
        self.iterationPath = '' # reset in the end
        self.pathToUseSource = '' # reset in the end
        self.replicaPath = replicaPath
        self.level = 0 # reset in the end
        self.mode = 0o666

    def reset(self) -> None:
        self.level = 0
        self.globaDirList.clear()
        self.localDirList.clear()
        self.newPath = ''
        self.iterationPath = ''
        self.pathToUseSource = ''

    def fileLevelModification(self, item, itemPath, replicaPath) -> None:
        # the it is some sort of file in that directory
                itemReplicaPath = os.path.join(replicaPath, str(item))
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
        if self.newPath == '': # very unstable way doing this check, but works (not using this right now anyways)
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
                self.fileLevelModification(item, itemPath, self.replicaPath)
        replicaItemsList = os.listdir(self.replicaPath)
        replicaItemsList = self.ignoreTempFiles(replicaItemsList)
        self.removalProcedure(itemsList, replicaItemsList, self.replicaPath)
        
        self.globaDirList.append(copy.deepcopy(self.localDirList))
        self.localDirList.clear()
        self.beginBFS()
        self.reset()
        s.enter(self.freq, 1, self.checkSource)
     
    def beginBFS(self)->None:
        for thisDir in self.globaDirList[self.level]:
            dirExtension = ''
            if str(thisDir).startswith(self.sourcePath):
                dirExtension = thisDir[len(self.sourcePath)+1:]
            lReplicaPath = os.path.join(self.replicaPath, dirExtension)
            if os.path.exists(lReplicaPath):
                # the directory exists check file status and add dir to localDirList
                # also check if any files or the directory was removed
                # if so remove that too.
                self.dirItemsCheck(thisDir, lReplicaPath)                      
            else:
                #the directory does not exists. create directory and copy all the items into it
                os.mkdir(lReplicaPath)
                self.dirItemsCheck(thisDir, lReplicaPath)
        if len(self.localDirList) > 0:
            self.globaDirList.append(copy.deepcopy(self.localDirList))
        self.localDirList.clear()
        self.level = self.level+1
        # print(self.globaDirList[self.level]) # do not unommnet index out of range. termination condition
        if len(self.globaDirList) == self.level:
            # bfs exhausted. all braches covered. do nothing END OF SEARCH
            pass
        else:
            self.beginBFS()
    
    def dirItemsCheck(self, thisDir, lReplicaPath) -> None:
        sourceItemsList = os.listdir(thisDir)
        sourceItemsList = self.ignoreTempFiles(sourceItemsList)
        for item in sourceItemsList: # check source directory items
            itemPath = os.path.join(thisDir, item) # create source dir items path
            if os.path.isfile(itemPath):
                self.fileLevelModification(item, itemPath, lReplicaPath) # copy items to replica path
            else:
                # it is a directory add it to the local dir for next round
                self.localDirList.append(itemPath)
        replicaItemsList = os.listdir(lReplicaPath)
        replicaItemsList = self.ignoreTempFiles(replicaItemsList)  
        self.removalProcedure(sourceItemsList, replicaItemsList, lReplicaPath)
                         
    def removalProcedure(self, sourceItemsList, replicaItemsList, lReplicaPath) -> None:
        for replicaItem in replicaItemsList:
            lReplicaItemPath = os.path.join(lReplicaPath, replicaItem)
            if sourceItemsList.__contains__(replicaItem):
                # no need to do anything. It is synchronised
                pass
            else:
                # the item has been deleted from the source remove it from here
                if os.path.isfile(lReplicaItemPath):
                    # remove the file
                    os.remove(lReplicaItemPath)
                else:
                    # remove the directory
                    shutil.rmtree(lReplicaItemPath, ignore_errors=True)
    
    def ignoreTempFiles(self, itemsList)->List:
        for item in itemsList:
                if item.startswith('~$'):
                    itemsList.remove(item)
        return itemsList
                
if __name__ == "__main__":
    
    sourceDist = input('Enter full path of source folder, where you will store files: \n')
    replicaDist = input('Enter full path of replica folder, where you want all data to be replicated: \n')
    freqs = input('Enter the frequency of periodic check (units: seconds): \n')
    freq = int(freqs)

    logging.basicConfig(filename='Logs.log', encoding='utf-8', level=logging.DEBUG)
    s=sched.scheduler(time.time, time.sleep)
  
    s.enter(freq, 1, SourceToReplicaManagement(freq, sourceDist, replicaDist).checkSource)
    s.run()
