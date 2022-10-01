import logging
import hashlib
import sched, time
import shutil
import os

class FileManagement():

    def __init__(self, freq, sourcePath, replicaPath) -> None:
        self.freq = freq
        self.completedOuterDirList = []
        self.sourcePath = sourcePath
        self.newPath = ''
        self.iterationPath = ''
        self.replicaPath = replicaPath
        self.block_size = 65536

    def fileLevelModification(self, item, itemPath) -> None:
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
                    2+2
                else:
                    #file does not exist, copy paste here
                    print('i am here')
                    logging.info('File duplicated \n')
                    shutil.copyfile(itemPath, itemReplicaPath)

    def checkDir(self)  -> None:
        print('just ran again')
        if self.newPath == '':
            itemsList = os.listdir(self.sourcePath)
            for item in itemsList:
                if item.startswith('~$'):
                    itemsList.remove(item)
        else:
            itemsList = os.listdir(self.iterationPath)
            for item in itemsList:
                if item.startswith('~$'):
                    itemsList.remove(item)

        for item in itemsList:
            itemPath = self.sourcePath + '/' + str(item)
            if os.path.isdir(itemPath) == True:
                # not a file but a directory
                self.iterationPath = itemPath
                self.completedOuterDirList.append(self.iterationPath)
            else:
                # a file
                self.fileLevelModification(item, itemPath)
        s.enter(self.freq, 1, self.checkDir)

    def removalProcedure(self)->None:
        # start from replica and see what is different in source
        2+2
                



#class Synchroniser(Digest):

#    def __init__(self, sourcePath, replicaPath) -> None:
#    super().__init__()
###

if __name__ == "__main__":
    sourceDist = input('Please enter the full path of source folder (where you will store files): \n')
    replicaDist = input('Please enter the full path of replica folder (where you want all data to be replicated): \n')
    logging.basicConfig(filename='Logs.log', encoding='utf-8', level=logging.DEBUG)
    s=sched.scheduler(time.time, time.sleep)
    freq = 60
    s.enter(freq, 1, FileManagement(freq, str(sourceDist), str(replicaDist)).checkDir)
    s.run()
