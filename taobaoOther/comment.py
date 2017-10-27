import taobaoOther.config
import utils.netUtils
import utils.utils
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
import requests

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class comment:
    taobaoToKen = []

    def getData(self, itemId,page=1):
        cookie=comment.getCookies();
        dict = {
            'url': taobaoOther.config.commentUrl.format(itemId,page),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': True,
            'reLoad': True,
            'isHeader':True,
            'isCookie':True,
            'putCookie':cookie['putCookie'],
            'header':{
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding":"gzip, deflate, br",
                "Connection":"keep-alive",
                "Upgrade-Insecure-Requests":"1",
                "Pragma":"no-cache",
                "Cache-Control":"no-cache"
            }
        }
        #print(dict)
        return self.getItemData(dict)

    def getItemData(self, dict):
        data = utils.netUtils.netUtils.getData(dict);
        #print(data['header']['Location'])
        if (data['isSuccess']):
            #print("成功:"+data['body'])
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], 'jsonp_tbcrate_reviews_list(')
                body = json.loads(jsonStr);

                if ('rateDetail' in body  and  body['rateDetail'] is not None and 'rateList' in body['rateDetail'] and len(body['rateDetail']['rateList']) > 0):
                    return json.dumps(body['rateDetail']['rateList']);
                else:
                    return self.getItemDataReLoad(dict);
            else:
                return None;
        elif (data['code'] ==302):
            print("302处理")
            return self.url302Handler(data['header']['Location']);
            #print(data['header']['Location'])
            pass
        else:
            print("失败，重试")
            return self.getItemDataReLoad(dict);

    # 单条内容获取失败重试
    def getItemDataReLoad(self, dict):
        # print(cookieArr[0])
        cookie = comment.getCookies()
        if (dict['reLoad']):
            dict['reLoad'] = False,
            dict['isCookie']=True,
            dict['putCookie'] =cookie['putCookie']
            return self.getItemData(dict);
        else:
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
        #print(cookie)
        if (dict['reLoad']):
            dict['putCookie'] = cookie
            dict['reLoad'] = False
            return self.getItemData(dict);

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
            return dict;
        else:
            cookie = {'cookie2': "",
                      '_tb_token_': "",
                      't': ""}
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
