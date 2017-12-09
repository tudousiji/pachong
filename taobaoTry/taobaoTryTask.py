import os
import sys

sys.path.append("..")
import taobaoTry.taobaoTryUtils
from task.logUtils import logUtils

class taobaoTryTask:

    def enum(**enums):
        return type('Enum', (), enums)
    taskType = enum(JingXuan=1, All=2)
    mTaskTypeFor = taskType.All
    taobaoTryTaskLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "taobaoTry.lock"
    def __init__(self,taskTypeFor=taskType.All):
        global mTaskTypeFor
        taobaoTryTask.mTaskTypeFor = taskTypeFor
        if(taskTypeFor==taobaoTryTask.taskType.JingXuan):
            taobaoTryTask.taobaoTryTaskLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "taobaoJingXuanTry.lock"
        else:
            taobaoTryTask.taobaoTryTaskLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "taobaoAllTry.lock"

        if (os.path.exists(taobaoTryTask.taobaoTryTaskLockFile)):
            if (taskTypeFor == taobaoTryTask.taskType.JingXuan):
                logUtils.info("精选类型文件已存在，即将退出")
            else:
                logUtils.info("所有类型文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            if (taskTypeFor == taobaoTryTask.taskType.JingXuan):
                logUtils.info("精选类型创建文件")
            else:
                logUtils.info("所有类型创建文件")
            open(taobaoTryTask.taobaoTryTaskLockFile, "w")
            if(taskTypeFor==taobaoTryTask.taskType.JingXuan):
                self.actionJingXuanTask()
            else:
                self.actionAllTask()


    def __del__(self):
        if (os.path.exists(taobaoTryTask.taobaoTryTaskLockFile)):
            os.remove(taobaoTryTask.taobaoTryTaskLockFile)
        if (taobaoTryTask.mTaskTypeFor == taobaoTryTask.taskType.JingXuan):
            logUtils.info("精选类型退出程序")
        else:
            logUtils.info("所有类型退出程序")

    def actionAllTask(self):
        logUtils.info("actionAllTask所有")
        taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, 0, 1)  # 第一个参数传入负数是精选，传0是所有的都采集

    def actionJingXuanTask(self):
        logUtils.info("actionAllTask精选")
        taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, -1, 1)  # 第一个参数传入负数是精选，传0是所有的都采集


# taobaoTryTask(taobaoTryTask.taskType.JingXuan).actionJingXuanTask()
taobaoTryTask(taobaoTryTask.taskType.JingXuan)
