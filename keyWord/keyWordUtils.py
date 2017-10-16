import keyWord.config
import utils.netUtils
from bs4 import BeautifulSoup
import utils.utils
import config.config
import json

class keyWordUtils:
    def getHotKeyWords(self):
        data = self.getLevel1();
        for items in data:
            self.parseLevel1Xls(items);


    def getLevel1(self):
        dict={
            'url':keyWord.config.level1Url,
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
        for type in keyWord.config.type:
            url= keyWord.config.getXlsUrl.format(id,type)
            data = utils.utils.utils.parseXls(url)
            for items in data:
                for index in range(2,len(items)):
                    if(len(items[index])>0 and items[index][0].isdigit()):
                        print(items[index][1])
                        list.append(items[index][1])
        self.postHotKeyWords(list)


    def postHotKeyWords(self,lists):
        #print(len((lists)))
        postDict = {
            'data': json.dumps(lists),
        }
        dict = {
            'url':config.config.addHotKeyWords,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        data  = utils.netUtils.netUtils.getData(dict)
        print(data)
        if(data['isSuccess']):
            print("提交服务器成功")
        else:
            print("提交服务器失败")
        print("----")
