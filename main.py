import os
import time
from concurrent.futures import ThreadPoolExecutor
import taobaoOther.baiduKeyWordsPos
import taobaoOther.askEveryBody
import task.taobaoTryTask
import taobaoBuyInventory.buyInventoryUtils
import task.taobaoOtherTask
import urllib.parse
import test.urlSafeCheck

#test.urlSafeCheck.urlSafeCheck().getData();

# url="http://www.qq.om/index.php?a=10&b=100"
# data=urllib.parse.urlparse(url).query
# data2=urllib.parse.parse_qs(data)
# print(data2)
for index in range(1, 2):
    data = taobaoBuyInventory.buyInventoryUtils.buyInventoryUtils().getData()
    print(data)
# import test.test4
#import test.test6
# task.taobaoOtherTask.taobaoOtherTask().actionTask()
#task.taobaoTryTask.taobaoTryTask(task.taobaoTryTask.taobaoTryTask.taskType.All)
#data=taobaoOther.askEveryBody.askEveryBody().getData(539342264315)
#task.taobaoInfo.taobaoInfo();
#aa=os.linesep
# data = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData("小米手机咋样呢，推荐表")
#print(data)
#utils.logUtils.logUtils.getData("main","dsfsfdsfsdfds递四方速递范德萨范德萨范德萨范德萨发生第三方的舒服舒服似懂非懂是范德萨发生发生范德萨范德萨发生的 的事发生地方")
#utils.logUtils.logUtils.getData("main","321")
#data=taobaoOther.askEveryBody.askEveryBody().getData(557806129437)
#taobaoOther.taobaoOtherUtils.taobaoOtherUtils().getData();
#data = taobaoOther.comment.comment().getData(557806129437)
#print(data)
# taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData("A-005多功能地面酒店用洗地机手推式地毯清洗机")
class main:

    def __init__(self):
        print("开始程序")
        if(os.path.exists('.lock')):
            print("文件已存在，即将退出")
            os._exit(0)
        else:
            #os.mknod('.lock')
            open('.lock',"w")

    def mainStart(self):
        for index in range(0,100):
            time.sleep(1)
            data = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData("小米手机双11清仓大促")
            print((str)(index)+"-->"+(str)(data))
            print("-------")

    def __del__(self):
        if (os.path.exists('.lock')):
            os.remove('.lock')
        print("退出程序")

#main().mainStart();

dict2 = {
            'url': 'http://2017.ip138.com/ic.asp',
            'requestType': 'GET',
            'isProxy': True,
            'isHttps': False,
            'proxyProtocol':'http',
            'proxyIp':'116.196.88.44',
            'proxyPort':'808',
        }

#ut = utils.netUtils.netUtils();
#data = ut.getData(dict2)
proxies = { "http": "http://116.196.88.44:808" }
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

head = {
            'Host', '2017.ip138.com',
            'User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language', ' zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding', 'deflate',
            'Referer', ' http://www.baidu.com',
            'Connection', ' keep-alive',
            'Cache-Control', ' max-age=0',
}

#r = requests.get(url=dict2['url'], proxies=proxies,headers=headers,timeout=60)
#print(r.encoding)
#print(r.text)#r.text.encode(r.encoding).decode('gbk')
#r.close()
#data = utils.netUtils.netUtils.getData(dict2);
#print(data);


#print(proxy.proxyUtils.proxyUtils.getLocalIp());





def return_future_result(message):
    #print(threading.Thread().getName())
    #time.sleep(10)
    #print("结束"+message)
    #print(proxy.proxyThreadSingleton.proxyThreadSingleton())
    #print(proxy.proxyThreadSingleton.proxyThreadSingleton().getSingleton())
    return message
pool = ThreadPoolExecutor(max_workers=50)  # 创建一个最大可容纳2个task的线程池
#for index in range(100):
    #pool.submit(return_future_result, ("hello1"))  # 往线程池里面加入一个task

#print(future1.done())  # 判断task1是否结束
#time.sleep(3)
#print(dir(pool))







#data=proxy.proxyUtils.proxyUtils.checkProxyIp();

#proxy.proxyThreadSingleton.proxyThreadSingleton().getSingleton().aa();

#utils.netUtils.netUtils.getTbkSign("c9dde6bb0fcacccb62b744a349f815e4","12574478",str(int(round(time.time() * 1000))),'{"pNum":3,"pSize":10,"floorId":"393","qId":"","channel":"zonghe","refpid":"mm_10011550_0_0","spm":"a3126.8759693/b.zhrx","couponSrc":"temai","app_pvid":"201_10.179.66.211_807926_1506749535487","ctm":"spm-url:"}')

