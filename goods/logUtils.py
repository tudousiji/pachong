import utils.logUtils
class logUtils:
    @staticmethod
    def info(*msg):
        info=""
        for indexs in range(len(msg)):
            info+=str(msg[indexs]);
        utils.logUtils.logUtils.info("goods",info)
