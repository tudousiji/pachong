import os
import sys

sys.path.append("..")
import taobaoBuyInventory.buyInventoryUtils
from task.logUtils import logUtils


class buyInventoryTask:
    buyInventoryTaskLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "buyInventory.lock"

    def __init__(self):

        if (os.path.exists(buyInventoryTask.buyInventoryTaskLockFile)):
            logUtils.info("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(buyInventoryTask.buyInventoryTaskLockFile, "w")

    def __del__(self):
        if (os.path.exists(buyInventoryTask.buyInventoryTaskLockFile)):
            os.remove(buyInventoryTask.buyInventoryTaskLockFile)
        logUtils.info("退出程序")

    def actionTask(self):
        taobaoBuyInventory.buyInventoryUtils.buyInventoryUtils().getData()


buyInventoryTask().actionTask()
