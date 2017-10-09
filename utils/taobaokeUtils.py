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
        data = taobaoProbation.config.data.format(page,cate)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoProbation.config.BeautySkinCareUrl.format(appConfig.appkey, times, sign, data)
        #print(url)
        return url;


    def handleDat(self,dict,page,cate):
        if(dict is None):
            cookieArr = None;
            cookiesDict = None;
            if (len(taobaokeUtils.taobaoToKen) > 0):
                index = random.randint(0, len(taobaokeUtils.taobaoToKen) - 1)
                cookiesDict = taobaokeUtils.taobaoToKen[index];
                cookieArr = dict['_m_h5_tk'].split('_')

            dict = {
                'url': self.getUrl(cookieArr[0] if cookieArr is not None else "", page, cate),
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoad':True,
            }
            if (cookiesDict is not None):
                dict['putCookie'] = cookiesDict
        self.getData(dict,page,cate);

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
                        cookie = {'_m_h5_tk': data['get_cookie']['_m_h5_tk'],
                                  '_m_h5_tk_enc': data['get_cookie']['_m_h5_tk_enc']}
                        taobaokeUtils.taobaoToKen.append(cookie)
                        #print(cookieArr[0])
                        if(dict['reLoad']):
                            dict['url'] = self.getUrl(cookieArr[0],page,cate);
                            dict['putCookie'] = cookie
                            dict['reLoad']=False
                            self.getData(dict, page, cate);
                        pass


