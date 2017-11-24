import utils.taobaokeUtils
import time
import taobaoOther.config
import config.config
import utils.netUtils
import json
import utils.utils
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
# from taobaoOther.logUtils import logUtils
import gc
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class askEveryBody:
    def getData(self, itemId, page=1):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getUrl(cookiesDict['cookies'],itemId);

        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }
        del cookiesDict
        del url
        return self.getItemData(dict, itemId);


    def getItemData(self,dict,itemId):

        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            if (data['body'] is not None):
                # jsonStr = data['body'][data['body'].index('mtopjsonp8(') + len('mtopjsonp8('):len(data['body']) - 1];
                #print(data['body'])
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp12(");
                body = json.loads(jsonStr)
                del jsonStr
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        del dict
                        del data
                        if('data' in body and 'cards' in body['data'] and len(body['data']['cards'])>0):
                            content = json.dumps(body['data']['cards'])
                            del body

                            return content;
                        else:
                            del body

                            return None
                    else:
                        dict['isCookie'] = True;
                        del body
                        if('_m_h5_tk' in  data['get_cookie']):
                            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
                        #print(data['get_cookie'])
                            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                            # print(cookieArr[0])
                            if (dict['reLoad']):
                                dict['url'] = self.getUrl(cookieArr[0], itemId);
                                dict['putCookie'] = cookie
                                dict['reLoad'] = False
                                del cookie
                                del data
                                del cookieArr
                                gc.collect()
                                return self.getItemData(dict,itemId);
                            else:
                                del data
                                del cookie
                                del cookieArr
                                del dict
                                gc.collect()
                                return None;
                        else:
                            del data
                            del dict
                            gc.collect()
                            return None
                else:
                    del dict
                    del jsonStr
                    del data
                    del body
                    gc.collect()
                    return None
            else:
                del data
                del dict
                gc.collect()
                return None
        else:

            del data
            del dict
            gc.collect()
            return None

    def getUrl(self,cookie,itemId,size=10,page=1):
        if (cookie is None):
            cookie = "";

        times = str(int(round(time.time() * 1000)));
        data = taobaoOther.config.askEveryBodyData.format(itemId, page)
        sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
        url = taobaoOther.config.askEveryBodyUrl.format(config.config.appkey, times, sign, data)
        del times
        del data
        del sign
        gc.collect()
        return url;