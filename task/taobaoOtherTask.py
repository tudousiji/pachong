import os
import task
import logging
import taobaoOther.taobaoOtherUtils

class taobaoOtherTask:
    taobaoLockFile = "lockFile" + os.path.sep + "taobaoInfo.lock"
    def __init__(self):

        if (os.path.exists(taobaoOtherTask.taobaoLockFile)):
            print("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(taobaoOtherTask.taobaoLockFile, "w")

    def __del__(self):
        if (os.path.exists(taobaoOtherTask.taobaoLockFile)):
            os.remove(taobaoOtherTask.taobaoLockFile)
        print("退出程序")

    def actionTask(self):
        taobaoOther.taobaoOtherUtils.taobaoOtherUtils().getData()
