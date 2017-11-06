import os
import goods.goodsList

class goodsTask:
    goodsTaskLockFile = "goods.lock"

    def __init__(self):

        if (os.path.exists(goodsTask.goodsTaskLockFile)):
            print("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(goodsTask.goodsTaskLockFile, "w")

    def __del__(self):
        if (os.path.exists(goodsTask.goodsTaskLockFile)):
            os.remove(goodsTask.goodsTaskLockFile)
        print("退出程序")

    def actionTask(self):
        goods.goodsList.goodsList().getData()