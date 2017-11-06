import os
import hotKeyWord.keyWordUtils

class hotKeyWordsTask:
    hotKeyWordsLockFile = "lockFile" + os.path.sep + "taobaoInfo.lock"

    def __init__(self):

        if (os.path.exists(hotKeyWordsTask.hotKeyWordsLockFile)):
            print("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(hotKeyWordsTask.hotKeyWordsLockFile, "w")

    def __del__(self):
        if (os.path.exists(hotKeyWordsTask.hotKeyWordsLockFile)):
            os.remove(hotKeyWordsTask.hotKeyWordsLockFile)
        print("退出程序")

    def actionTask(self):
        hotKeyWord.keyWordUtils.keyWordUtils().getHotKeyWords()