import utils.taobaokeUtils
import goods.config
import time
import config.config
import utils.netUtils
import json

class goodsList:
    def getData(self,keyWords):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getUrl(cookiesDict['cookies'], keyWords);

        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }
        return self.getItemData( dict,keyWords);

    def getItemData(self,dict,keyWords):

        data=utils.netUtils.netUtils.getData(dict)

        if (data['isSuccess']):
            #print("成功:"+data['body'])
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)
                if (str(body['ret']).startswith("['FAIL_") is not True):
                    return json.dumps(body);
                elif(dict['reLoad'] is True):
                    dict['isCookie'] = True;
                    cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                    return self.getItemDataReLoad(dict,keyWords);
                else:
                    return None;
            else:
                return None;

        elif(dict['reLoad'] is True):
            return self.getItemDataReLoad(dict,keyWords);
        else:
            return None

            # 单条内容获取失败重试

    def getItemDataReLoad(self, dict,keyWords):
        cookie = utils.taobaokeUtils.taobaokeUtils.getCookies()
        url = self.getUrl(cookie['cookies'], keyWords);

        if (dict['reLoad']):
            dict['url'] = url;
            dict['reLoad'] = False;
            dict['isCookie'] = True;
            dict['putCookie'] = cookie['putCookie'];
            return self.getItemData(dict,keyWords);
        else:
            return None;

    def getUrl(self,cookie,keyWords,size=10,page=1):
        if (cookie is None):
            cookie = "";
        times = str(int(round(time.time() * 1000)));
        dataStr=(str)(goods.config.taobaoke_keyword_url_data);
        data = dataStr % (keyWords, (page-1)*size,size,config.config.pid,config.config.pid)
        sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
        dataUrlStr = str(goods.config.taobaoke_keyword_url)
        url = dataUrlStr % (config.config.appkey, times, sign, data)
        return url;