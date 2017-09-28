import socket;
import proxy.proxyThreadSingleton
import utils


from concurrent.futures import ThreadPoolExecutor
import time
import threading

dict2 = {
            'url': 'http://2017.ip138.com/ic.asp',
            'requestType': 'GET',
            'isProxy': True,
            'isHttps': False,
            'proxyProtocol':'http',
            'proxyIp':'60.23.39.219',
            'proxyPort':'80',
        }

#ut = utils.netUtils.netUtils();
#data = ut.getData(dict)
#print(data)


#print(proxy.proxyUtils.proxyUtils.getLocalIp());




s1= proxy.proxyThreadSingleton.proxyThreadSingleton();
s2= proxy.proxyThreadSingleton.proxyThreadSingleton().getSingleton();
print(s1)
print(s2)
exit;

def return_future_result(message):
    #print(threading.Thread().getName())
    #time.sleep(10)
    #print("结束"+message)
    print(proxy.proxyThreadSingleton.proxyThreadSingleton())
    print(proxy.proxyThreadSingleton.proxyThreadSingleton().getSingleton())
    return message
pool = ThreadPoolExecutor(max_workers=50)  # 创建一个最大可容纳2个task的线程池
for index in range(100):
    pool.submit(return_future_result, ("hello1"))  # 往线程池里面加入一个task

#print(future1.done())  # 判断task1是否结束
#time.sleep(3)
#print(dir(pool))
print("继续呀")




dict = {
            'url': 'http://www.xicidaili.com/nn/{0}',
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'index': 1,
            'reLoad':True,
        }
data=proxy.proxyUtils.proxyUtils.getProxyList(dict);
