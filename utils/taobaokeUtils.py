import taobaoProbation.config
import config.config as appConfig
import utils.netUtils
import time
import urllib.request
import json
import random

class taobaokeUtils:
    taobaoToKen=[]

    def getUrl(self,cookie,page,cate):
        if (cookie is None):
            cookie = "";
        data = taobaoProbation.config.data.format(page,cate)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoProbation.config.BeautySkinCareUrl.format(appConfig.appkey, times, sign, data)
        #print(url)
        return url;


    def handleDat(self,dict,page,cate):

        if(dict is None):
            cookies=self.getCookies();
            cookiesStr = cookies['cookies'];
            cookiesDict = cookies['putCookie'];


            dict = {
                'url': self.getUrl(cookiesStr if cookiesStr is not None else "", page, cate),
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoad':True,
            }
            if (cookiesDict is not None):
                dict['putCookie'] = cookiesDict
        self.getData(dict,page,cate);

    #获取淘宝客cookies
    @staticmethod
    def getCookies():
        if (len(taobaokeUtils.taobaoToKen) > 0):
            index = random.randint(0, len(taobaokeUtils.taobaoToKen) - 1)
            cookiesDict = taobaokeUtils.taobaoToKen[index];
            cookieArr = cookiesDict['_m_h5_tk'].split('_')
            dict = {
                'cookies':cookieArr[0],
                'putCookie':cookiesDict
            }
            return dict;
        else:
            cookie = {'_m_h5_tk': "",
                      '_m_h5_tk_enc': ""}
            dict = {
                'cookies': None,
                'putCookie': None
            }
            return dict

    #设置cookies
    @staticmethod
    def putCookies(cookies):
        cookie = {'_m_h5_tk': cookies['_m_h5_tk'],
                  '_m_h5_tk_enc': cookies['_m_h5_tk_enc']}
        taobaokeUtils.taobaoToKen.append(cookie)
        return cookie


    def getData(self,dict,page,cate):
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = data['body'][data['body'].index('mtopjsonp8(') + len('mtopjsonp8('):len(data['body']) - 1];
                body = json.loads(jsonStr)
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        pass
                        #print(type(body['data']['module']))
                        #if(body['data'] is not None and type(body['data']['module']) is list and len(body['data']['module'])>0
                        #   and type(body['data']['module']['moduleData']) is list and
                         #          len(body['data']['module']['moduleData'])>0):
                         #   for items in body['data']['module']['moduleData']:
                         #       print("111")
                         #       print(type(body['data']['module']['moduleData']))


                    else:
                        dict['isCookie'] = True;
                        cookieArr = data['get_cookie']['_m_h5_tk'].split('_')

                        cookie = self.putCookies(data['get_cookie']);
                        #print(cookieArr[0])
                        if(dict['reLoad']):
                            dict['url'] = self.getUrl(cookieArr[0],page,cate);
                            dict['putCookie'] = cookie
                            dict['reLoad']=False
                            self.getData(dict, page, cate);
                        pass


