from bs4 import BeautifulSoup
import json
import utils.netUtils
import re
import config.config
import proxy.proxyThreadSingleton

class proxyUtils:
    @staticmethod
    def getProxyList():
        dict = {
            'url': config.config.getProxyList,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'index': 1,
            'reLoad': True,
        }
        proxyUtils.proxyList(dict);


    @staticmethod
    def proxyList(dict):

        #contentDict = {'ip': '113.120.132.122', 'port': '8118', 'type': 'http'}
        #proxyUtils.checkProxyStatus(contentDict);
        #return ;

        url = dict['url'].format(dict['index'])
        dict['url'] = url;
        ut = utils.netUtils.netUtils();
        data = ut.getData(dict)
        if(data['isSuccess']):
            soup = BeautifulSoup(data['body'], "html.parser")
            nowplaying_movie = soup.find('table', id="ip_list")
            if(nowplaying_movie is not None and len(nowplaying_movie)>0):
                nowplaying_movie_list = nowplaying_movie.find_all('tr')
                if(nowplaying_movie_list is not None and len(nowplaying_movie_list)>0):
                    successProxyList = [];
                    failProxyList = [];
                    for items in nowplaying_movie_list:
                        # item=items.find_all('tr');
                        country = items.find(attrs={'class': 'country'});
                        if (country is not None):
                            if (country.get_text() != "国家"):
                                content = items.find_all('td');
                                ip = content[1].get_text();
                                port = content[2].get_text();
                                city = content[3].get_text().replace("\n", "").strip();
                                serviceType = content[4].get_text();
                                type = content[5].get_text();
                                contentDict = {'ip': ip, 'port': port, 'city': city, 'serviceType': serviceType, 'type':type}
                                #isValid =proxyUtils.checkProxyStatus(contentDict);#检查是否有效
                                singLeton = proxy.proxyThreadSingleton.proxyThreadSingleton();
                                singLeton.setData(contentDict)
                                #return ;
                                #if (isValid):
                                #    successProxyList.append(contentDict)
                                #else:
                                #    failProxyList.append(contentDict)
                    #请求网络写入数据库

                    dict['index'] = dict['index']+1;
                    #proxy.proxyThreadSingleton.proxyThreadSingleton().setSuccessList(None)
                    #print(len(successProxyList));
                    #print(successProxyList);
                    #print('------------')
                    #print(len(failProxyList));
                    #print(failProxyList);

                    proxyUtils.getProxyList(dict)
                else:
                    index=0
            else:
                index=0
        elif (dict['reLoad']):
            dict['reLoad'] = False;
            proxyUtils.getProxyList(dict)

    index=0;

    #检查代理ip的状态
    @staticmethod
    def checkProxyStatus(contentDict):
        dict = {
            'url': config.config.checkProxyStatusUrl,
            'requestType': 'GET',
            'isProxy': True,
            'isHttps': False,
            'proxyProtocol':contentDict['type'],
            'proxyIp':contentDict['ip'],
            'proxyPort':contentDict['port'],
        }
        #print(dict)
        ut = utils.netUtils.netUtils();
        data = ut.getData(dict)

        if(data['isSuccess']):
            body=data['body'];
            soup = BeautifulSoup(body, "html.parser")
            nowplaying_movie = soup.find('center')
            if(nowplaying_movie is not None):
                text=nowplaying_movie.get_text();
                ip =proxyUtils. drawIp(text)
                if(ip is not None and ip !=proxyUtils.getLocalIp()):
                    return True
        return False;


    #ip提取
    @staticmethod
    def drawIp(text):
        if (text is not None):
            ip = re.findall('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', text);
            return ip[0]
        return None

    # 批量从服务器获取代理ip并检查代理ip的状态
    @staticmethod
    def checkProxyIp(dict=None):
        if(dict is None):
            dict = {
                'url': config.config.getNextProxyIpList,
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'index': 1,
                'reLoad': True,
            }
        url = dict['url'].format(dict['index'])
        dict['url'] = url;
        ut = utils.netUtils.netUtils();
        data = ut.getData(dict)
        if (data['isSuccess'] is True):
            jsonObj=json.loads(data['body'])
            if(jsonObj['Code']==0):
                failProxyIpList=[]
                for items in jsonObj['data']:
                    dict={
                        'ip':items['ip'],
                        'port': items['port'],
                        'type':'http' if items['http_type']==0 else 'https',
                    }
                    isValid = proxy.proxyThreadSingleton.proxyThreadSingleton().checkProxyStatus(dict)
                    if(isValid is False):
                        failProxyIpDict={
                            'id':items['id']
                        }
                        failProxyIpList.append(failProxyIpDict);
                if(len(failProxyIpList)>0):
                    dictList = {
                        'url': config.config.updateFailProxyIp,
                        'requestType': 'POST',
                        'isProxy': False,
                        'isHttps': False,
                        'postData': json.dumps(failProxyIpList),
                        'reLoad': True,
                    }
                    proxyUtils.updateFailProxyIp(dictList);
        elif dict['reLoad'] is True :
            dict['reLoad']=False;
            proxyUtils.checkProxyIp(dict);
        return True;


    @staticmethod
    def updateFailProxyIp(dictList):



        ut = utils.netUtils.netUtils();
        data = ut.getData(dictList)
        if(data['isSuccess'] is True):
            jsonObj = json.loads(data['body'])
            if (jsonObj['Code'] != 0 and dictList['reLoad'] is True):
                dictList['reLoad'] = False;
                proxyUtils.checkProxyIp(dict);
        elif dict['reLoad'] is True:
            dictList['reLoad'] = False;
            proxyUtils.checkProxyIp(dictList);