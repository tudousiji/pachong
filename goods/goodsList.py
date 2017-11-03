import utils.taobaokeUtils
import goods.config
import time
import config.config
import utils.netUtils
import json

class goodsList:
    pageSize=100;
    def getData(self,page=1):
        dict = {
            'url': config.config.getKeyWordsList.format(page,goodsList.pageSize),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        self.getKeyWordslit(dict,page);

    def getKeyWordslit(self,dict,page):
        print("采集列表:",dict['url'])
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            #print("成功:"+data['body'])
            if (data['body'] is not None):
                body=json.loads(data['body'])
                for item in body:
                    data = self.getGoodsData(item['keyword'])
                    if(data is not None):
                        dict={
                            'keyword_id':item['id'],
                            'data':data
                        }
                        print("成功:" , dict)
                        self.postData(dict)
                    else:
                        print("内容失败")

                if(len(body)>=goodsList.pageSize):
                    nextPage=page+1;
                    dict['url']=config.config.getKeyWordsList.format(nextPage,goodsList.pageSize)
                    self.getKeyWordslit(dict,nextPage)
                else:
                    print("采集结束")
            else:
                return None
        else:
            return None


    def postData(self,dict):
        data = utils.utils.utils.postDataForService(dict, config.config.addGoodsItem)
        if(data['isSuccess']):
            print("服务器提交成功")
        else:
            print("服务器提交失败:",data)

    def getGoodsData(self,keyWords):
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
        print("采集内容:", dict['url'])
        data=utils.netUtils.netUtils.getData(dict)

        if (data['isSuccess']):

            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)
                if (str(body['ret']).startswith("['FAIL_") is not True):
                    # if('data' in body and 'data' in body['data'] and 'auctionList' in body['data']['data'] and 'auctions' in body['data']['data']['auctionList']):
                    #     return body['data']['data']['auctionList']['auctions'];
                    # else:
                    #
                    #     return None
                    return body
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

    def getUrl(self,cookie,keyWords,size=1000,page=1):
        if (cookie is None):
            cookie = "";
        times = str(int(round(time.time() * 1000)));
        dataStr=(str)(goods.config.taobaoke_keyword_url_data);
        data = dataStr % (keyWords, (page-1)*size,size,config.config.pid,config.config.pid)
        sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
        dataUrlStr = str(goods.config.taobaoke_keyword_url)
        url = dataUrlStr % (config.config.appkey, times, sign, data)
        return url;