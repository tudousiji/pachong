
import os
import time
class logUtils:

    logFileTime=None
    logRootDirectory="."+os.path.sep+"logDirectory"+os.path.sep

    @staticmethod
    def info(moduleName=None,msg=None):
        if (moduleName is None or msg is None):
            errMsg="发生异常,moduleName or msg is empty";
            print(errMsg)
            logUtils.mkFile(logUtils.logRootDirectory+"glob.txt",errMsg)
            return

        dir=logUtils.getDir(moduleName);
        logUtils.mkFile(dir, msg)

    @staticmethod
    def getDir(moduleName):
        localTime = time.localtime(time.time());
        logDirectory = time.strftime('%Y-%m-%d', localTime)
        if (os.path.exists(logUtils.logRootDirectory +moduleName+ os.path.sep+ logDirectory) is False):
            os.makedirs(logUtils.logRootDirectory +moduleName+ os.path.sep+ logDirectory)
        timeNowFile = time.strftime("%Y-%m-%d %H_%M", localTime)
        timeNowFile = timeNowFile[:-1] + "0.txt"
        dir = logUtils.logRootDirectory +moduleName+ os.path.sep + logDirectory + os.path.sep + timeNowFile
        return dir;

    @staticmethod
    def mkFile(fileName,msg):
        print(fileName+"文件写入:\r\n"+msg)
        f = open(fileName, 'a', encoding='utf-8')
        localTime = time.localtime(time.time());
        writeTime=time.strftime('%Y-%m-%d %H:%M:%S', localTime)
        f.write("["+writeTime+"] "+msg+'\n')
        f.newlines
        f.close()
        print("----------------")