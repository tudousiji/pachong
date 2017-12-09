import os
import sys

sys.path.append("..")
import goods.goodsList
from task.logUtils import logUtils

print(os.getcwd())  # 获得当前工作目录
exit(0)
class goodsTask:
    goodsTaskLockFile = ".." + os.path.sep + "lockFile" + os.path.sep + "goods.lock"

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


goodsTask().actionTask();
