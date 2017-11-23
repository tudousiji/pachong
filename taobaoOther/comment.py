import taobaoOther.config
import utils.netUtils
import utils.utils
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
import requests
import config.config
from taobaoOther.logUtils import logUtils
import gc
import traceback
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class comment:
    taobaoToKen = []

    def getData(self, itemId,page=1):
        # cookie=comment.getCookies();
        dict = {
            'url': taobaoOther.config.commentUrl.format(itemId,page),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': True,
            'reLoad': True,
            'taskType': config.config.taskType.COMMENT,
            # 'isHeader':True,
            # 'isCookie':True,
            # 'putCookie':cookie['putCookie'],
            # 'header':{
            #     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            #     "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            #     "Accept-Encoding":"gzip, deflate, br",
            #     "Connection":"keep-alive",
            #     "Upgrade-Insecure-Requests":"1",
            #     "Pragma":"no-cache",
            #     "Cache-Control":"no-cache"
            # }
        }
        #print(dict)

        return self.getItemData(dict)

    def getItemData(self, dict):

        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):

            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], 'jsonp_tbcrate_reviews_list(')
                try:
                    body = json.loads(jsonStr);
                    del data
                    del jsonStr

                    if ('rateDetail' in body and body['rateDetail'] is not None and 'rateList' in body[
                        'rateDetail'] and len(body['rateDetail']['rateList']) > 0):
                        content = json.dumps(body['rateDetail']['rateList'])
                        del body
                        gc.collect()
                        return content;
                    elif (dict['reLoad'] is True):
                        del body
                        gc.collect()
                        return self.getItemDataReLoad(dict);
                    else:
                        del body
                        gc.collect()
                        return None;
                except Exception as err:

                    gc.collect()
                    errorData = traceback.format_exc()
                    utils.logUtils.logUtils.info("error", str(errorData));
                    return None;
            else:
                del data
                gc.collect()
                return None;
        elif (data['code'] ==302):
            logUtils.info("302处理")
            Location = data['header']['Location']
            del data
            return self.url302Handler(Location);
            #print(data['header']['Location'])
            pass
        else:
            del data
            logUtils.info("失败，重试")
            return self.getItemDataReLoad(dict);

    # 单条内容获取失败重试
    def getItemDataReLoad(self, dict):
        # print(cookieArr[0])
        cookie = comment.getCookies()
        if (dict['reLoad']):
            dict['reLoad'] = False,
            dict['isCookie']=True,
            dict['putCookie'] =cookie['putCookie']
            del cookie
            return self.getItemData(dict);
        else:
            del dict
            del cookie
            return None;


    def url302Handler(self,url):
        #print("url:"+url)
        cookie=comment.getCookies();
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': True,
            'isCookie': True,
            'reLoad': True,
            'putCookie': cookie['putCookie'],
            'isHeader': True,
        }

        data = utils.netUtils.netUtils.getData(dict);
        dict['isCookie'] = True;
        #print("设置cookie"+(str)(data['get_cookie'])+"-->"+(str)(len(data['get_cookie'])))
        if(data['get_cookie'] is not  None and len(data['get_cookie'])==3):
            cookie = comment.putCookies(data['get_cookie']);
        else:
            getCook=comment.getCookies()
            cookie = getCook['putCookie'];
            del getCook
        del data
        #print(cookie)
        if (dict['reLoad']):
            dict['putCookie'] = cookie
            dict['reLoad'] = False
            del cookie
            return self.getItemData(dict);
        else:
            del cookie
            del dict
            return None

    # 获取淘宝客cookies
    @staticmethod
    def getCookies():
        if (len(comment.taobaoToKen) > 0):
            index = random.randint(0, len(comment.taobaoToKen) - 1)
            cookiesDict = comment.taobaoToKen[index];
            dict = {
                'putCookie': cookiesDict,
                'index': index,
            }
            del index
            del cookiesDict

            return dict;
        else:
            # cookie = {'cookie2': "",
            #          '_tb_token_': "",
            #          't': ""}
            dict = {
                'cookies': None,
                'putCookie': None
            }
            return dict

    # 设置cookies
    @staticmethod
    def putCookies(cookies):
        cookie = {'cookie2': cookies['cookie2'],
                  '_tb_token_': cookies['_tb_token_'],
                  't': cookies['t'],
                  }

        comment.taobaoToKen.append(cookie)
        return cookie

    @staticmethod
    def reMoveCookies(index):
        del comment.taobaoToKen[index]
