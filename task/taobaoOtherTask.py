import os
import sys

sys.path.append("..")
import taobaoOther.taobaoOtherUtils
from task.logUtils import logUtils

class taobaoOtherTask:
    taobaoLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "taobaoInfo.lock"
    def __init__(self):

        if (os.path.exists(taobaoOtherTask.taobaoLockFile)):
            logUtils.info("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            logUtils.info("创建文件")
            open(taobaoOtherTask.taobaoLockFile, "w")

    def __del__(self):
        if (os.path.exists(taobaoOtherTask.taobaoLockFile)):
            os.remove(taobaoOtherTask.taobaoLockFile)
        logUtils.info("退出程序")

    def actionTask(self):
        taobaoOther.taobaoOtherUtils.taobaoOtherUtils().getData()


taobaoOtherTask().actionTask();
