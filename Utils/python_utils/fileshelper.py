import os
import sys
from datetime import datetime

CURRENT_DATETIME = datetime.now()

class FileHelper():
    """docstring for FileHelper"""
    def __init__(self, logPath, storeArea, ifeos=False):
        self.ifeos = ifeos
        self.logPath = logPath
        self.storeArea = storeArea
        self.dirName=(str(CURRENT_DATETIME.year)[-2:]
                      +str(format(CURRENT_DATETIME.month,'02d'))
                      +str(format(CURRENT_DATETIME.day,'02d'))
                      +"_"
                      +str(format(CURRENT_DATETIME.hour,'02d'))
                      +str(format(CURRENT_DATETIME.minute,'02d'))
                      +str(format(CURRENT_DATETIME.second,'02d'))
                      )
        self.eosString = '/eos/uscms'
        print "==> Time stamp: ",self.dirName

    def CreateLogDirWithDate(self):
        """Member function to create directory to store log files.

        Returns:
            [type] -- [description]
        """
        LogDirName = str(self.logPath)+os.sep+str(self.dirName)
        os.system('mkdir -p '+ LogDirName)
        print "==> Created directory for log files: ",LogDirName
        return LogDirName

    def CreateSotreArea(self,path):
        """Create directory in the store area.

        Arguments:
            path {string} -- Name of directory with path

        Returns:
            string -- created directory in the store area

        """
        os.system('xrdfs root://cmseos.fnal.gov/ mkdir '+path)
        print "==> Created dire at eos path: ",path
        return path

    def createStoreDirWithDate(self, additionalString1="", additionalString2="", additionalString3=""):
        """Function to create the store area.

        [description]

        Keyword Arguments:
            additionalString1 {str} -- additional args (default: {""})
            additionalString2 {str} -- additional args2 (default: {""})
            additionalString3 {str} -- additional args3 (default: {""})

        Returns:
            string -- returns the path of created directory.
        """
        path = self.CreateSotreArea(self.storeArea)
        if additionalString1 != "":
            path = self.CreateSotreArea(path + os.sep + additionalString1)
        if additionalString2 != "":
            path = self.CreateSotreArea(path + os.sep + additionalString2)
        if additionalString3 != "":
            path = self.CreateSotreArea(path + os.sep + additionalString3)
        path = self.CreateSotreArea(path + os.sep + self.dirName) # append dateTime stamp at the end
        return path

    def CreateDirWithDate(self):
        """create both log and store area

        [description]

        Returns:
            string -- first string contains name of log directory
            string -- second string contains name of store area directory
        """
        logDirName = str(self.logPath)+os.sep+str(self.dirName)
        storeAreaDirName1 = str(self.storeArea)
        storeAreaDirName2 = str(self.storeArea) + os.sep + str(self.dirName)
        os.system('mkdir -p '+ logDirName)
        os.system('xrdfs root://cmseos.fnal.gov/ mkdir '+storeAreaDirName1)
        os.system('xrdfs root://cmseos.fnal.gov/ mkdir '+storeAreaDirName2)
        print "==> Created directory for log files: ",logDirName
        print "==> Created dire at eos path: ",storeAreaDirName2
        return logDirName, storeAreaDirName2
