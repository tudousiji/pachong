import os
import taobaoTry.taobaoTryUtils

class taobaoTryTask:
    def enum(**enums):
        return type('Enum', (), enums)
    taskType = enum(JingXuan=1, All=2)

    taobaoTryTaskLockFile = "taobaoTry.lock"
    def __init__(self,taskTypeFor=taskType.All):
        if(taskTypeFor==taobaoTryTask.taskType.JingXuan):
            taobaoTryTask.taobaoTryTaskLockFile="taobaoJingXuanTry.lock"
        else:
            taobaoTryTask.taobaoTryTaskLockFile = "taobaoAllTry.lock"

        if (os.path.exists(taobaoTryTask.taobaoTryTaskLockFile)):
            print("文件已存在，即将退出")
            os._exit(0)
        else:
            # os.mknod('.lock')
            print("创建文件")
            open(taobaoTryTask.taobaoTryTaskLockFile, "w")
            if(taskTypeFor==taobaoTryTask.taskType.JingXuan):
                self.actionJingXuanTask()
            else:
                self.actionAllTask()


    def __del__(self):
        if (os.path.exists(taobaoTryTask.taobaoTryTaskLockFile)):
            os.remove(taobaoTryTask.taobaoTryTaskLockFile)
        print("退出程序")

    def actionAllTask(self):
        taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, 0,1)  # 第二个参数传入负数是精选，传0是所有的都采集

    def actionJingXuanTask(self):
        taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, 0, -1)  # 第二个参数传入负数是精选，传0是所有的都采集