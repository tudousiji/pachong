import utils.taobaokeUtils
import time
import taobaoOther.config
import config.config
import utils.netUtils
import json
import utils.utils
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests

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
        return self.getItemData(dict, itemId);


    def getItemData(self,dict,itemId):
        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            if (data['body'] is not None):
                # jsonStr = data['body'][data['body'].index('mtopjsonp8(') + len('mtopjsonp8('):len(data['body']) - 1];
                #print(data['body'])
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp12(");

                body = json.loads(jsonStr)
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        if('data' in data and 'cards' in data['data']):
                            return json.dumps(body);
                        else:
                            return None
                    else:
                        dict['isCookie'] = True;
                        if('_m_h5_tk' in  data['get_cookie']):
                            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
                        #print(data['get_cookie'])
                            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                            # print(cookieArr[0])
                            if (dict['reLoad']):
                                dict['url'] = self.getUrl(cookieArr[0], itemId);
                                dict['putCookie'] = cookie
                                dict['reLoad'] = False
                                return self.getItemData(dict,itemId);
                            else:
                                return None;
                        else:
                            return None
                else:
                    return None
            else:
                return None
        else:
            return None

    def getUrl(self,cookie,itemId,size=10,page=1):
        if (cookie is None):
            cookie = "";

        times = str(int(round(time.time() * 1000)));
        data = taobaoOther.config.askEveryBodyData.format(itemId, page)
        sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
        url = taobaoOther.config.askEveryBodyUrl.format(config.config.appkey, times, sign, data)
        return url;