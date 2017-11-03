import taobaoOther.config
import utils.netUtils
import utils.utils
import json
import random
import config.config
import urllib.parse
import logging


class baiduKeyWordsPos:
    baiduToKen = []
    maxKeyWordsCount=5;
    def getData(self,keyword):
        cookie=self.getCookies();

        dict = {
            'url': taobaoOther.config.baiduKeyWordsPos.format(urllib.parse.quote(keyword) ),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            #'putCookie':cookie['putCookie'],
            'taskType':config.config.taskType.BAIDU,
        }
        return self.getItemData(dict)

    def getItemData(self,dict):
        data = utils.netUtils.netUtils.getData(dict);
        if(data['isSuccess']):
            if (data['body'] is not None):
                body=json.loads(data['body']);
                if('result' in body and "res" in body['result'] and "keyword_list" in body['result']['res']):
                    #if (data['get_cookie'] is not None and len(data['get_cookie']) > 0):
                    #    cookie = self.putCookies(data['get_cookie']);
                    if(len(body['result']['res']['keyword_list'])>=baiduKeyWordsPos.maxKeyWordsCount):
                        return json.dumps(body['result']['res']['keyword_list'])
                    else:
                        #keyWordsList=[];
                        keyWordsList=(body['result']['res']['keyword_list'])
                        itemList=[];
                        for item in body['result']['res']['wordrank'] :
                            item2=item.split(":");
                            if(len(item2[0])>=2 and item2[0].isdigit() is False):
                                itemList.append(item2)

                        itemList.sort(key=lambda x: x[1],reverse=True)
                        for item in itemList:
                            if(item[0] not in keyWordsList):
                                keyWordsList.append(item[0])
                            if(len(keyWordsList)>=baiduKeyWordsPos.maxKeyWordsCount):
                                break
                        return json.dumps(keyWordsList)
                else:
                    return self.isReLoad(data,dict);
            else:
                return self.isReLoad(data,dict);
        else:
            return self.isReLoad(data,dict);

    def isReLoad(self,data,dict):
        if(dict['reLoad']):
            dict['reLoad']=False;

            if (data['get_cookie'] is not None and len(data['get_cookie']) >0):
                cookie = self.putCookies(data['get_cookie']);
            else:
                getCook = self.getCookies()
                cookie = getCook['putCookie'];
            dict['putCookie'] = cookie
            return self.getItemData(dict);
        else:
            return None;


    # 获取淘宝客cookies
    def getCookies(self):
        if (len(baiduKeyWordsPos.baiduToKen) > 0):
            index = random.randint(0, len(baiduKeyWordsPos.baiduToKen) - 1)
            cookiesDict = baiduKeyWordsPos.baiduToKen[index];
            dict = {
                'putCookie': cookiesDict,
                'index': index,
            }
            return dict;
        else:

            dict = {
                'putCookie': None
            }
            return dict

    # 设置cookies

    def putCookies(self,cookies):
        print("putCookies:"+(str)(cookies))
        cookie = {'BAIDUID': cookies['BAIDUID'],
                  }
        #if(cookie not in baiduKeyWordsPos.baiduToKen):
        baiduKeyWordsPos.baiduToKen.clear();
        baiduKeyWordsPos.baiduToKen.append(cookie)
        #else:
        #    print("这个cookies已存在")
        return cookie


    def reMoveCookies(self,index):
        del baiduKeyWordsPos.baiduToKen[index]





