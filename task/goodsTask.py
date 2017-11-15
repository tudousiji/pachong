import os
import goods.goodsList
import os
from task.logUtils import logUtils

class goodsTask:
    goodsTaskLockFile = "lockFile" + os.path.sep + "goods.lock"

    def __init__(self):

        if (os.path.exists(goodsTask.goodsTaskLockFile)):
            logUtils.info("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(goodsTask.goodsTaskLockFile, "w")

    def __del__(self):
        if (os.path.exists(goodsTask.goodsTaskLockFile)):
            os.remove(goodsTask.goodsTaskLockFile)
        logUtils.info("退出程序")

    def actionTask(self):
        goods.goodsList.goodsList().getData()
