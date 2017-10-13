import taobaoTry.config
import utils.utils
import time
import config.config as appConfig
import utils.netUtils
import utils.taobaokeUtils
import json
import config.config
from bs4 import BeautifulSoup
import urllib.parse

class taobaoTryUtils:

    def getUrl(self,cookie,page,cate):
        if (cookie is None):
            cookie = "";
        data = taobaoTry.config.data.format(page, cate)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoTry.config.BeautySkinCareUrl.format(appConfig.appkey, times, sign, data)
        #print(url)
        return url;


    #wap版本采集（未完成）
    def handleWapDat(self,dict,page,cate):

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
                'cookiesInfoDict':cookies
            }
            if (cookiesDict is not None):
                dict['putCookie'] = cookiesDict
        self.getData(dict,page,cate);


    def handlePcTryList(self,dict,index=0,page=1):
        if (dict is None):

            cate=taobaoTry.config.cateList[index];
            indexStr=str(index);
            #print("cate:"+indexStr)

            dict = {
                'url': taobaoTry.config.taobaoTryList.format(cate,page),
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoad': True,
            }

        self.parsePcTaobaoTryList(dict, index,page);


    def parsePcTaobaoTryList(self,dict,index,page):
        #print("url:"+dict['url'])
        cate = taobaoTry.config.cateList[index];
        dict['url']=taobaoTry.config.taobaoTryList.format(cate,page);
        data = utils.netUtils.netUtils().getData(dict)
        if (data['isSuccess']):
            soup = BeautifulSoup(data['body'], "html.parser")
            content = soup.find('div', class_="tb-try-pg-report-list")
            item_list=content.find_all('div',class_="report-item");
            if(len(item_list)>0):
                for items in item_list:
                    #report_item = items.find('div', class_="report-item");
                    report_item_wrap=items.find('a',class_="report-item-wrap")
                    title=report_item_wrap.find('span',class_="writer").find('span',class_="title")

                    href = report_item_wrap['href']
                    result = urllib.parse.urlparse(href)
                    params = urllib.parse.parse_qs(result.query, True)
                    itemId = params['itemId'][0];
                    reportId= params['reportId'][0]
                    print(" title:"+title.getText()+" cate:"+str(taobaoTry.config.cateList[index])+" page:"+str(page)+" itemId:"+itemId+" reportId:"+reportId+" url:"+dict['url'])
                    self.getItemData(None,reportId,itemId)

                nextPage = page + 1
                print(dict['url'] + "采集成功，下一页:" + str(nextPage));
                dict['reLoad'] = True;
                self.parsePcTaobaoTryList(dict, index, nextPage)
            else:#下一个列表
                dict['reLoad'] = True;
                nextIndex=index+1;
                if(len(taobaoTry.config.cateList)>nextIndex):
                    print(dict['url'] + "采集下一个分类:"+str(nextIndex))
                    self.parsePcTaobaoTryList(dict, nextIndex, 1)
                else:
                    print("列表采集结束")
        else:
            if(dict['reLoad']):
                print(dict['url']+"采集失败，重试中")
                dict['reLoad']=False;
                self.parsePcTaobaoTryList(dict,index,page)
            else:
                nextPage=page+1
                print(dict['url'] + "采集失败，下一页:"+str(nextPage));
                dict['reLoad'] = True;
                self.parsePcTaobaoTryList(dict, index,nextPage )



    def getItemUrl(self,cookie,id,itemId):
        if (cookie is None):
            cookie = "";
        data = taobaoTry.config.itemData.format(itemId, id)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoTry.config.BeautySkinCareUrl.format(appConfig.appkey, times, sign, data)
        #print(url)
        return url;

    def getItemData(self,dict,id,itemId):
        cookies = utils.taobaokeUtils.taobaokeUtils.getCookies();
        cookiesStr = cookies['cookies'];
        cookiesDict = cookies['putCookie'];
        if(dict is None):
            dict = {
                'url': self.getItemUrl(cookiesStr if cookiesStr is not None else "", id, itemId),
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoad': True,
                'putCookie':cookiesDict,
                'isCookie':True,
                'cookiesInfoDict': cookies,
                'reLoad':True
            }
        if (cookiesDict is not None):
            dict['putCookie'] = cookiesDict
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'],'mtopjsonp8(')
                print(jsonStr)
                print("---------------")
                body = json.loads(jsonStr)
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        pass#服务器上发数据
                        data = body['data']['module'][0]['moduleData']
                        dict ={
                            'data':data,
                            'itemId':data['tryItemId'],
                            'tryId':data['reportId'],
                        }
                        #print(data)
                        #utils.utils.utils.postDataForService(data,config.config.addTaobaoTryUrl)
                    else:
                        if (dict.get('cookiesInfoDict')):
                            if (dict.get('cookiesInfoDict').get('index')):
                                utils.taobaokeUtils.taobaokeUtils.reMoveCookies(dict['cookiesInfoDict']['index'])

                        dict['isCookie'] = True;
                        #cookieArr = data['get_cookie']['_m_h5_tk'].split('_')

                        utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                        cookies = utils.taobaokeUtils.taobaokeUtils.getCookies();
                        cookiesStr = cookies['cookies'];
                        cookiesDict = cookies['putCookie'];
                        # print(cookieArr[0])
                        if (dict['reLoad']):
                            dict['url'] = self.getItemUrl(cookiesStr if cookiesStr is not None else "", id, itemId);
                            dict['putCookie'] = cookiesDict
                            dict['reLoad'] = False
                            self.getItemData(dict, id,itemId);



    def getData(self,dict,page,cate):
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = data['body'][data['body'].index('mtopjsonp8(') + len('mtopjsonp8('):len(data['body']) - 1];
                body = json.loads(jsonStr)
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        pass
                        data=json.loads(jsonStr)
                        #print(data['data']['module'][0]['moduleData'])
                        for index in range(len(data['data']['module'][0]['moduleData']))  :
                            id = data['data']['module'][0]['moduleData'][index]['id']
                            itemId=data['data']['module'][0]['moduleData'][index]['itemId']
                            self.getItemData(id,itemId)



                    else:

                        if(dict.get('cookiesInfoDict')):
                            if(dict.get('cookiesInfoDict').get('index')):
                                utils.taobaokeUtils.reMoveCookies(dict['cookiesInfoDict']['index'])


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