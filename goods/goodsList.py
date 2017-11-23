import utils.taobaokeUtils
import goods.config
import time
import config.config
import utils.netUtils
import utils.utils
import json
import gc
from goods.logUtils import logUtils
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
        logUtils.info("采集列表:",dict['url'])
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            #print("成功:"+data['body'])
            if (data['body'] is not None):
                body=json.loads(data['body'])
                for item in body:
                    goodsData = self.getGoodsData(item['keyword'])
                    if (goodsData is not None):
                        dict={
                            'keyword_id':item['id'],
                            'data': goodsData
                        }
                        del goodsData
                        logUtils.info("成功:", " 关键词Id:", item['id'], " 关键词:", item['keyword'], dict)
                        self.postData(dict)
                    else:
                        del goodsData
                        logUtils.info("内容失败")

                if(len(body)>=goodsList.pageSize):
                    del body
                    nextPage=page+1;
                    dict['url']=config.config.getKeyWordsList.format(nextPage,goodsList.pageSize)
                    self.getKeyWordslit(dict,nextPage)
                else:
                    del body
                    logUtils.info("采集结束")
            else:
                del data
                return None
        else:
            del data
            return None


    def postData(self,dict):
        data = utils.utils.utils.postDataForService(dict, config.config.addGoodsItem)
        if(data['isSuccess']):
            logUtils.info("服务器提交成功")
        else:
            logUtils.info("服务器提交失败:",data)
        del dict
        del data
        gc.collect()

    def getGoodsData(self,keyWords):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getUrl(cookiesDict['cookies'], keyWords, goods.config.goodsPageSize);

        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }
        del url
        del cookiesDict
        return self.getItemData( dict,keyWords);

    def getItemData(self,dict,keyWords):

        data=utils.netUtils.netUtils.getData(dict)
        logUtils.info("采集内容:", dict['url'])
        if (data['isSuccess']):

            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");

                body = json.loads(jsonStr)
                if (str(body['ret']).startswith("['FAIL_") is not True):
                    del data
                    # if('data' in body and 'data' in body['data'] and 'auctionList' in body['data']['data'] and 'auctions' in body['data']['data']['auctionList']):
                    #     return body['data']['data']['auctionList']['auctions'];
                    # else:
                    #
                    #     return None
                    gc.collect()
                    return body
                elif(dict['reLoad'] is True):
                    del body
                    dict['isCookie'] = True;
                    cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                    del data
                    del cookie
                    gc.collect()
                    return self.getItemDataReLoad(dict,keyWords);
                else:
                    del data
                    del body
                    gc.collect()
                    return None;
            else:
                del data
                gc.collect()
                return None;

        elif(dict['reLoad'] is True):
            del data
            gc.collect()
            return self.getItemDataReLoad(dict,keyWords);
        else:
            del data
            gc.collect()
            return None

            # 单条内容获取失败重试

    def getItemDataReLoad(self, dict,keyWords):
        cookie = utils.taobaokeUtils.taobaokeUtils.getCookies()
        url = self.getUrl(cookie['cookies'], keyWords, goods.config.goodsPageSize);

        if (dict['reLoad']):
            dict['url'] = url;
            dict['reLoad'] = False;
            dict['isCookie'] = True;
            dict['putCookie'] = cookie['putCookie'];
            del url
            del cookie
            return self.getItemData(dict,keyWords);
        else:
            del url
            del cookie
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
        del times
        del dataStr
        del data
        del sign
        return url;