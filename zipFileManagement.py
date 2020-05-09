# importing csv module 
import os
import zipfile

class zipFileManagement(object):
    def __init__(self, zipFileName, pathToOutputFolderDirectory):
        self.zipFileName = zipFileName
        self.pathToOutputFolderDirectory = pathToOutputFolderDirectory
        self.outPutFolderName = "output"
        self.createOutputFolder()
        self.pathToOutputFolder = os.path.join(self.pathToOutputFolderDirectory, self.outPutFolderName)

    def getZipFilePath(self):
        return os.path.join(self.pathToOutputFolder, self.zipFileName)

    def getZipFileName(self):
        return self.zipFileName

    def createOutputFolder(self):
        if not os.path.exists(os.path.join(self.pathToOutputFolderDirectory, self.outPutFolderName)):
            os.mkdir(os.path.join(self.pathToOutputFolderDirectory, self.outPutFolderName))

    def createZipFileFromOutputFolder(self):
        # calling function to get all file paths in the directory 
        file_paths = self.get_all_file_paths()
    
        # writing files to a zipfile 
        with zipfile.ZipFile(self.getZipFilePath(),'w') as zip: 
            # writing each file one by one 
            for file in file_paths: 
                zip.write(file)

    def emptyOutputFolder(self):
        filelist = [ f for f in os.listdir(self.pathToOutputFolder) ]
        for file in filelist:
            # print("FILE: " + file)
            os.remove(os.path.join(self.pathToOutputFolder, file))

    def get_all_file_paths(self): 
        # initializing empty file paths list 
        file_paths = []
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(self.pathToOutputFolder): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(self.pathToOutputFolder, filename) 
                file_paths.append(filepath) 
        # returning all file paths 
        return file_paths 


