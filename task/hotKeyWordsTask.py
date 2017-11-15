import os
import hotKeyWord.keyWordUtils
from task.logUtils import logUtils

class hotKeyWordsTask:
    hotKeyWordsLockFile = "lockFile" + os.path.sep + "taobaoInfo.lock"

    def __init__(self):

        if (os.path.exists(hotKeyWordsTask.hotKeyWordsLockFile)):
            logUtils.info("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            logUtils.info("创建文件")
            open(hotKeyWordsTask.hotKeyWordsLockFile, "w")

    def __del__(self):
        if (os.path.exists(hotKeyWordsTask.hotKeyWordsLockFile)):
            os.remove(hotKeyWordsTask.hotKeyWordsLockFile)
        logUtils.info("退出程序")

    def actionTask(self):
        hotKeyWord.keyWordUtils.keyWordUtils().getHotKeyWords()