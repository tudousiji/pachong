import utils.taobaokeUtils

import config.config
import utils.netUtils
import json
import taobaoOther.config
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class taobaoSubKeyWords:
    pageSize = 100;

    def getData(self, page=1):
        dict = {
            'url': config.config.getKeyWordsForSubKeyWordsNullList.format(page, taobaoSubKeyWords.pageSize),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        self.getSubKeyWordsList(dict, page);

    def getSubKeyWordsList(self, dict, page):
        print("采集列表:", dict['url'])
        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            # print("成功:"+data['body'])
            if (data['body'] is not None):
                body = json.loads(data['body'])
                for item in body:
                    print(body)
                    print("item:",item)
                    data = self.getSubKeyWordsData((str)(item['keyword']))
                    if (data is not None and 'result' in data and len(data['result'])>0):
                        print("成功:", data)
                        dict={
                            'id':item['id'],
                            'data':data
                        }
                        self.postData(dict)
                    else:
                        print("内容失败")

                if (len(body) >= taobaoSubKeyWords.pageSize):
                    nextPage = page + 1;
                    dict['url'] = config.config.getKeyWordsForSubKeyWordsNullList.format(nextPage, taobaoSubKeyWords.pageSize)
                    self.getSubKeyWordsList(dict, nextPage)
                else:
                    print("采集结束")
            else:
                return None
        else:
            return None

    def postData(self, dict):
        print(dict)
        data = utils.utils.utils.postDataForService(dict, config.config.addKeyWordsForSubKeyWordsNull)
        if (data['isSuccess']):
            print("服务器提交成功")
        else:
            print("服务器提交失败:", data)
        print("--------------------------")

    def getSubKeyWordsData(self, keyWords):
        url = taobaoOther.config.taobaoSubKeyWords.format(keyWords)
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        return self.getItemData(dict, keyWords);

    def getItemData(self, dict, keyWords):
        print("采集内容:", dict['url'])
        data = utils.netUtils.netUtils.getData(dict)

        if (data['isSuccess']):

            if (data['body'] is not None):
                body = json.loads(data['body'])
                return body;
            else:
                return None;

        elif (dict['reLoad'] is True):
            return self.getItemDataReLoad(dict, keyWords);
        else:
            return None

            # 单条内容获取失败重试

    def getItemDataReLoad(self, dict, keyWords):
        cookie = utils.taobaokeUtils.taobaokeUtils.getCookies()
        url = self.getUrl(cookie['cookies'], keyWords);

        if (dict['reLoad']):
            dict['url'] = url;
            dict['reLoad'] = False;
            dict['isCookie'] = True;
            dict['putCookie'] = cookie['putCookie'];
            return self.getItemData(dict, keyWords);
        else:
            return None;