import threading
from concurrent.futures import ThreadPoolExecutor
import utils.netUtils
from bs4 import BeautifulSoup
import proxy.proxyUtils
import re
import json

class proxyThreadSingleton(object):
    __instant = None;
    __lock = threading.Lock();
    __pool = None
    __ThreadCount=100
    localIp = None;
    __successList=[];
    __maxSuccessListCount=1;

    def __new__(self):
        if (proxyThreadSingleton.__instant == None):
            proxyThreadSingleton.__lock.acquire();
            if (proxyThreadSingleton.__instant == None):
                if (proxyThreadSingleton.__pool == None):
                    proxyThreadSingleton.__pool=ThreadPoolExecutor(proxyThreadSingleton.__ThreadCount);
                proxyThreadSingleton.__instant = object.__new__(self);
                proxyThreadSingleton.__lock.release()
        return proxyThreadSingleton.__instant

    def getSingleton(self):
        if proxyThreadSingleton.__instant is None:
            proxyThreadSingleton.__instant = proxyThreadSingleton()
        return proxyThreadSingleton.__instant


    def checkProxyStatus(self,contentDict):
        dict = {
            'url': 'http://2017.ip138.com/ic.asp', #http://2017.ip138.com/ic.asp  http://httpbin.org/ip
            'requestType': 'GET',
            'isProxy': True,
            'isHttps': False,
            'proxyProtocol':contentDict['type'],
            'proxyIp':contentDict['ip'],#'116.196.88.44',#contentDict['ip'],
            'proxyPort':contentDict['port']#'808',#contentDict['port'],
        }

        ut = utils.netUtils.netUtils();
        data = ut.getData(dict)
        #print(data)
        if(data['isSuccess']):
            body=data['body'];
            soup = BeautifulSoup(body, "html.parser")
            nowplaying_movie = soup.find('center')
            if(nowplaying_movie is not None):
                text=nowplaying_movie.get_text();

                ip =self.drawIp(text)
                #print(ip)
                if(ip is not None and ip !=self.getLocalIp()):
                    return True
        return False;

    def setData(self,contentDict):
        self.__pool.submit(self.handleData, (contentDict))
        #print(dir(self.__pool.map))
        #print(self.__pool.map)


    def handleData(self,contentDict):


        isValid=self.checkProxyStatus(contentDict);
        #print(contentDict['ip']+":"+contentDict['port']);
        #print(isValid)
        if(isValid):
            self.setSuccessList(contentDict);

        #print("------------------------")


    def setSuccessList(self,contentDict):
        proxyThreadSingleton.__lock.acquire();
        if(contentDict is not None):
            if (contentDict['type'] == 'http'):
                contentDict['type'] = 0;
            else:
                contentDict['type'] = 1;
            self.__successList.append(contentDict)
        if(len(self.__successList)>=self.__maxSuccessListCount or contentDict is None):
            if(self.__submitDataList()  or contentDict is None ):
                self.__successList=[]
        proxyThreadSingleton.__lock.release()

    def __submitDataList(self):#请求数据map
        print("发起请求网络")
        #print()

        postDict={
            'data':json.dumps(self.__successList),
        }
        dict = {
            'url': 'http://mytaobaoke/index.php/api/Proxyip/addProxyIp',
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData':postDict,
            'reLoad': True,
        }
        data = utils.netUtils.netUtils.getData(dict)
        #print(data)
        return True

    #测试方法
    def aa(self):
        dict={
            'port':20,
            'ip':'21.32.123',
            'type':'0'
        }
        self.setDictList(dict)
        self.setDictList(dict)
        self.__submitDataList();

    # 测试方法
    def setDictList(self,dict):
        if(dict['type'] == 'http'):
            dict['type']=0;
        else:
            dict['type'] = 1;
        self.__successList.append(dict)

    def getLocalIp(self):
        if (self.localIp is None):
            proxyThreadSingleton.__lock.acquire();
            if (self.localIp is None):
                dict = {
                    'url': 'http://2017.ip138.com/ic.asp',
                    'requestType': 'GET',
                    'isProxy': False,
                    'isHttps': False,
                    'reLoad': True,
                }
                data = utils.netUtils.netUtils().getData(dict)
                # print("请求网络 ")
                if (data['isSuccess']):
                    body = data['body'];
                    soup = BeautifulSoup(body, "html.parser")
                    nowplaying_movie = soup.find('center')
                    if (nowplaying_movie is not None):
                        text = nowplaying_movie.get_text();
                        ip = self.drawIp(text)
                        if (ip is not None):
                            self.localIp = ip
            proxyThreadSingleton.__lock.release()
        return self.localIp;

    def drawIp(self,text):
        if (text is not None):
            ip = re.findall('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', text);
            return ip[0]
        return None

