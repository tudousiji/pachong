import utils.taobaokeUtils

import config.config
import utils.netUtils
import json
import taobaoOther.config
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from taobaoOther.logUtils import logUtils
import gc
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
        logUtils.info("采集列表:", dict['url'])
        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            # print("成功:"+data['body'])
            if (data['body'] is not None):
                body = json.loads(data['body'])
                for item in body:
                    logUtils.info(body)
                    logUtils.info("item:",item)
                    subKeyWordsData = self.getSubKeyWordsData((str)(item['keyword']))
                    if (subKeyWordsData is not None and 'result' in subKeyWordsData and len(
                            subKeyWordsData['result']) > 0):
                        logUtils.info("成功:", data)
                        dict={
                            'id':item['id'],
                            'data': subKeyWordsData
                        }
                        self.postData(dict)
                    else:
                        logUtils.info("内容失败")
                    del subKeyWordsData
                del body
                if (len(body) >= taobaoSubKeyWords.pageSize):
                    del body
                    nextPage = page + 1;
                    dict['url'] = config.config.getKeyWordsForSubKeyWordsNullList.format(nextPage, taobaoSubKeyWords.pageSize)
                    self.getSubKeyWordsList(dict, nextPage)
                else:
                    del body
                    logUtils.info("采集结束")
            else:
                del data
                return None
        else:
            del data
            return None

    def postData(self, dict):
        logUtils.info(dict)
        data = utils.utils.utils.postDataForService(dict, config.config.addKeyWordsForSubKeyWordsNull)
        if (data['isSuccess']):
            logUtils.info("服务器提交成功")
        else:
            logUtils.info("服务器提交失败:", data)
        del data
        del dict
        gc.collect()
        logUtils.info("--------------------------")

    def getSubKeyWordsData(self, keyWords):
        url = taobaoOther.config.taobaoSubKeyWords.format(keyWords)
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        del url
        return self.getItemData(dict, keyWords);

    def getItemData(self, dict, keyWords):
        logUtils.info("采集内容:", dict['url'])
        data = utils.netUtils.netUtils.getData(dict)

        if (data['isSuccess']):
            del dict
            if (data['body'] is not None):
                body = json.loads(data['body'])
                del data

                return body;
            else:
                del data

                return None;

        elif (dict['reLoad'] is True):
            del data
            return self.getItemDataReLoad(dict, keyWords);
        else:
            del data
            del dict
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
            del url
            del cookie
            return self.getItemData(dict, keyWords);
        else:
            del url
            del dict
            del keyWords
            del cookie
            return None;