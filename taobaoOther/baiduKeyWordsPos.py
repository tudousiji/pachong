import taobaoOther.config
import utils.netUtils
import utils.utils
import json
import random
import config.config
import urllib.parse
from taobaoOther.logUtils import logUtils
import traceback
import gc


# A-005多功能地面酒店用洗地机手推式地毯清洗机
class baiduKeyWordsPos:
    baiduToKen = []
    maxKeyWordsCount = 5;

    def getData(self, keyword):
        logUtils.info("baiduKeyWordsPos getData")
        # cookie=self.getCookies();
        if (keyword is None or len(keyword) <= 0):
            return None
        dict = {
            'url': taobaoOther.config.baiduKeyWordsPos.format(urllib.parse.quote(keyword)),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            # 'putCookie':cookie['putCookie'],
            'taskType': config.config.taskType.BAIDU,
        }
        return self.getItemData(dict)

    def getItemData(self, dict):
        logUtils.info("baiduKeyWordsPos getItemData")
        data = utils.netUtils.netUtils.getData(dict);
        logUtils.info("baiduKeyWordsPos getItemData 222")
        if (data['isSuccess']):
            if (data['body'] is not None):
                body = None;
                try:
                    body = json.loads(data['body']);

                except Exception as err:
                    utils.logUtils.logUtils.info("error", data['body']);
                    errorData = traceback.format_exc()
                    utils.logUtils.logUtils.info("error", str(errorData));

                logUtils.info("baiduKeyWordsPos body:" + str(body));
                if (body is not None and 'result' in body and body['result'] is not None and "res" in body['result'] and
                            body['result']['res'] is not None and "keyword_list" in
                    body['result']['res']):
                    del data
                    # if (data['get_cookie'] is not None and len(data['get_cookie']) > 0):
                    #    cookie = self.putCookies(data['get_cookie']);

                    if (body['result']['res']['keyword_list'] is not None and len(
                            body['result']['res']['keyword_list']) >= baiduKeyWordsPos.maxKeyWordsCount):
                        content = json.dumps(self.handleList(body['result']['res']['keyword_list']))
                        del body
                        del dict
                        gc.collect()
                        return content
                    else:
                        if (body['result']['res']['keyword_list'] is not None):
                            # keyWordsList=[];
                            keyWordsList = (body['result']['res']['keyword_list'])
                            itemList = [];
                            for item in body['result']['res']['wordrank']:
                                item2 = item.split(":");
                                if (len(item2[0]) >= 2 and item2[0].isdigit() is False):
                                    itemList.append(item2)
                                del item2

                            itemList.sort(key=lambda x: x[1], reverse=True)
                            for item in itemList:
                                if (item[0] not in keyWordsList):
                                    keyWordsList.append(item[0])
                                if (len(keyWordsList) >= baiduKeyWordsPos.maxKeyWordsCount):
                                    break
                            content = json.dumps(self.handleList(keyWordsList))
                            del keyWordsList
                            del itemList
                            del body
                            del dict
                            gc.collect()
                            return content
                        else:
                            del body
                            del dict
                            gc.collect()
                            return None;
                else:

                    del body
                    gc.collect()
                    return self.isReLoad(data, dict);
            else:
                return self.isReLoad(data, dict);
        else:
            return self.isReLoad(data, dict);

    def isReLoad(self, data, dict):
        logUtils.info("baiduKeyWordsPos isReLoad")
        if (dict['reLoad']):
            dict['reLoad'] = False;
            cookie = None
            if (data['get_cookie'] is not None and len(data['get_cookie']) > 0):
                # cookie = self.putCookies(data['get_cookie']);
                pass
            else:
                getCook = self.getCookies()
                cookie = getCook['putCookie'];
                del getCook
            dict['putCookie'] = cookie
            del data
            del cookie
            gc.collect()
            return self.getItemData(dict);
        else:
            del data
            gc.collect()
            return None;

    # 获取淘宝客cookies
    def getCookies(self):
        logUtils.info("baiduKeyWordsPos getCookies")
        if (len(baiduKeyWordsPos.baiduToKen) > 0):
            index = random.randint(0, len(baiduKeyWordsPos.baiduToKen) - 1)
            cookiesDict = baiduKeyWordsPos.baiduToKen[index];
            dict = {
                'putCookie': cookiesDict,
                'index': index,
            }
            del cookiesDict
            del index
            return dict;
        else:

            dict = {
                'putCookie': None
            }
            return dict

    # 设置cookies

    def putCookies(self, cookies):
        logUtils.info("baiduKeyWordsPos putCookies")
        logUtils.info("putCookies:" + (str)(cookies))
        cookie = {'BAIDUID': cookies['BAIDUID'],
                  }
        # if(cookie not in baiduKeyWordsPos.baiduToKen):
        baiduKeyWordsPos.baiduToKen.clear();
        baiduKeyWordsPos.baiduToKen.append(cookie)
        # else:
        #    print("这个cookies已存在")
        return cookie

    def reMoveCookies(self, index):
        logUtils.info("baiduKeyWordsPos reMoveCookies")
        del baiduKeyWordsPos.baiduToKen[index]

    def getKeyWords(self):
        logUtils.info("baiduKeyWordsPos getKeyWords")
        list = config.config.keyWordsExtendList;
        size = len(list)
        index = random.randint(0, size - 1)
        keyword = list[index]
        del index
        del size
        del list
        return keyword;

    def handleList(self, list):
        logUtils.info("baiduKeyWordsPos handleList")
        size = len(list)
        index = random.randint(0, size - 1)
        list.insert(index, self.getKeyWords())
        del size
        del index
        return list;
