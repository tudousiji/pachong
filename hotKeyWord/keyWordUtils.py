import hotKeyWord.config
import utils.netUtils
from bs4 import BeautifulSoup
import utils.utils
import config.config
import json
from hotKeyWord.logUtils import logUtils
import gc
class keyWordUtils:
    def getHotKeyWords(self):
        data = self.getLevel1();
        for items in data:
            self.parseLevel1Xls(items);


    def getLevel1(self):
        dict={
            'url':hotKeyWord.config.level1Url,
            'requestType': 'GET'
        }
        data= utils.netUtils.netUtils.getData(dict)
        list = [];
        if (data['isSuccess']):
            soup = BeautifulSoup(data['body'], "html.parser")
            content = soup.find('div', class_="drop-list fd-hide")
            a = content.find_all('a')
            for items in a:
                id = items['data-key']
                list.append(id)
        return list

    def parseLevel1Xls(self,id):
        list = [];
        for type in hotKeyWord.config.type:
            url= hotKeyWord.config.getXlsUrl.format(id, type)
            data = utils.utils.utils.parseXls(url)
            del url
            for items in data:
                for index in range(2,len(items)):
                    if(len(items[index])>0 and items[index][0].isdigit()):
                        logUtils.info(items[index][1])
                        list.append(items[index][1])
            del data
        self.postHotKeyWords(list)
        del list


    def postHotKeyWords(self,lists):
        #print(len((lists)))
        postDict = {
            'data': json.dumps(lists),
        }
        del lists
        dict = {
            'url':config.config.addHotKeyWords,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        del postDict
        data  = utils.netUtils.netUtils.getData(dict)
        del dict
        logUtils.info(data)
        if(data['isSuccess']):
            logUtils.info("提交服务器成功")
        else:
            logUtils.info("提交服务器失败")
        del data
        gc.collect()
        logUtils.info("----")
