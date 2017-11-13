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
from taobaoTry.logUtils import logUtils
import taobaoOther.baiduKeyWordsPos

class taobaoTryUtils:
    jingXuanMaxPage=3;#精选最大页数
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

    #有分类的 定时运行
    def handlePcTryList(self,dict,index=0,page=1):
        if (dict is None):
            if(index>=0):
                self.getTryCate();
                cate=taobaoTry.config.cateList[index];
            else:
                cate="";
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


    def getTryCate(self):
        dict = {
            'url': config.config.getTryCate,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }

        jsonStr = utils.netUtils.netUtils.getData(dict)

        if(jsonStr['isSuccess']):
            data = json.loads(jsonStr['body'])
            #print(data)
            if(data['Status']):
                taobaoTry.config.cateList=data['data']
                logUtils.info(taobaoTry.config.cateList)



    def parsePcTaobaoTryList(self,dict,index,page):
        #print("url:"+dict['url'])
        if(index>=0):
            cate = taobaoTry.config.cateList[index];
        else:
            cate="";

        dict['url']=taobaoTry.config.taobaoTryList.format(cate,page);
        data = utils.netUtils.netUtils().getData(dict)
        if (data['isSuccess']):
            soup = BeautifulSoup(data['body'], "html.parser")
            content = soup.find('div', class_="tb-try-pg-report-list")
            item_list=content.find_all('div',class_="report-item");
            if(len(item_list)>0):
                list=[];
                for items in item_list:
                    #report_item = items.find('div', class_="report-item");
                    report_item_wrap=items.find('a',class_="report-item-wrap")
                    title=report_item_wrap.find('span',class_="writer").find('span',class_="title")
                    href = report_item_wrap['href']
                    result = urllib.parse.urlparse(href)
                    params = urllib.parse.parse_qs(result.query, True)
                    itemId = params['itemId'][0];
                    reportId= params['reportId'][0]
                    idDict={
                        'itemId':itemId,
                        'reportId':reportId,
                        'title':title.getText()
                    }
                    list.append(idDict)

                effectiveList=self.checkEffectiveList(list)
                if(effectiveList is not None or index<0):
                    if(len(effectiveList['data'])>0):
                        for items in effectiveList['data']:
                            itemId = items['itemId'];
                            reportId = items['reportId'];
                            title=items['title'];
                            logUtils.info(
                                " title:" + title + " cate:" + str(taobaoTry.config.cateList[index]) + " page:" + str(
                                    page) + " itemId:" + itemId + " reportId:" + reportId + " url:" + dict['url'])
                            self.getItemData(None,cate,reportId,itemId)
                        if(effectiveList['isNextCate'] is True):
                            dict['reLoad'] = True;
                            nextIndex = index + 1;
                            if ( ( len(taobaoTry.config.cateList) > nextIndex and index>=0)):
                                logUtils.info(dict['url'] + "采集下一个分类:" + str(nextIndex))
                                self.parsePcTaobaoTryList(dict, nextIndex, 1)
                            else:
                                logUtils.info("采集完成")
                            return
                if((index<0 and page>=taobaoTryUtils.jingXuanMaxPage)):
                    logUtils.info("采集完成")
                    return
                else:
                    nextPage = page + 1
                    if(effectiveList is not None):
                        logUtils.info(dict['url'] + "采集成功，下一页:" + str(nextPage));
                    else:
                        logUtils.info(dict['url'] + "采集失败，下一页:" + str(nextPage));
                    dict['reLoad'] = True;
                    self.parsePcTaobaoTryList(dict, index, nextPage)
            else:#下一个列表
                dict['reLoad'] = True;
                nextIndex=index+1;
                if(len(taobaoTry.config.cateList)>nextIndex):
                    logUtils.info(dict['url'] + "采集下一个分类:" + str(nextIndex))
                    self.parsePcTaobaoTryList(dict, nextIndex, 1)
                else:
                    logUtils.info("列表采集结束")
        else:
            if(dict['reLoad']):
                logUtils.info(dict['url'] + "采集失败，重试中")
                dict['reLoad']=False;
                self.parsePcTaobaoTryList(dict,index,page)
            else:
                nextPage=page+1
                logUtils.info(dict['url'] + "采集失败，下一页:" + str(nextPage));
                dict['reLoad'] = True;
                self.parsePcTaobaoTryList(dict, index,nextPage )

    #判断是否已经采集过了
    def checkEffectiveList(self,list):
        postDict = {
            'data': json.dumps(list),
        }
        dict = {
            'url': config.config.checkEffectiveTaobaoTryIdListUrl,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        data= utils.netUtils.netUtils.getData(dict)
        if (data['isSuccess']):
            return json.loads(data['body']);
        else:
            if(dict['reLoad']):
                dict['reLoad']=False
                self.checkEffectiveList(list)
            else:
                return None


    def getItemUrl(self,cookie,reportId,itemId):
        if (cookie is None):
            cookie = "";
        data = taobaoTry.config.itemData.format(itemId, reportId)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoTry.config.BeautySkinCareUrl.format(appConfig.appkey, times, sign, data)
        #print(url)
        return url;

    def getItemData(self,dict,cate,reportId,itemId):
        cookies = utils.taobaokeUtils.taobaokeUtils.getCookies();
        cookiesStr = cookies['cookies'];
        cookiesDict = cookies['putCookie'];
        if(dict is None):
            dict = {
                'url': self.getItemUrl(cookiesStr if cookiesStr is not None else "", reportId, itemId),
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
                #print(dict['url'])
                #print(jsonStr)
                body = json.loads(jsonStr)
                if (body is not None and str(body['ret']).startswith("['FAIL_") is not True and len(body['data']['module'][0]['moduleData'])>0):
                        pass#服务器上发数据
                        datas = body['data']['module'][0]['moduleData']
                        logUtils.info(datas)
                        dict ={
                            'data':datas,
                            'itemId':datas['tryItemId'],
                            'reportId':datas['reportId'],
                            'cate': cate,
                            # 'keywords': taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData(datas['item']['title']),
                        }
                        if (datas is not None and 'item' in datas and datas['item'] is not None and 'title' in datas[
                            'item'] and datas['item']['title'] is not None):
                            dict['keywords'] = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData(
                                datas['item']['title']);
                        #print(data)
                        statusStr = utils.utils.utils.postDataForService(dict,config.config.addTaobaoTryUrl)
                        #print(statusStr)
                        if(statusStr['isSuccess']):
                            status =json.loads(statusStr['body'])
                            if(statusStr['isSuccess'] and status['Code']==0):
                                logUtils.info("提交服务器成功")
                            else:
                                logUtils.info("提交服务器失败")
                            logUtils.info("---------------")
                        else:
                            utils.utils.utils.postDataForService(dict, config.config.addTaobaoTryUrl)

                else:
                    self.getItemDataReLoad(data,dict,cate, reportId, itemId)
            else:
                self.getItemDataReLoad(data,dict,cate, reportId, itemId)
        else:
            self.getItemDataReLoad(data,dict,cate, reportId, itemId)


    #单条内容获取失败重试
    def getItemDataReLoad(self,data,dict,cate,id,itemId):
        if (dict.get('cookiesInfoDict')):
            if (dict.get('cookiesInfoDict').get('index')):
                utils.taobaokeUtils.taobaokeUtils.reMoveCookies(dict['cookiesInfoDict']['index'])

        dict['isCookie'] = True;
        # cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
        if(data['get_cookie'] is not None):
            utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
        cookies = utils.taobaokeUtils.taobaokeUtils.getCookies();
        cookiesStr = cookies['cookies'];
        cookiesDict = cookies['putCookie'];
        # print(cookieArr[0])
        if (dict['reLoad']):
            dict['url'] = self.getItemUrl(cookiesStr if cookiesStr is not None else "", id, itemId);
            dict['putCookie'] = cookiesDict
            dict['reLoad'] = False
            self.getItemData(dict,cate, id, itemId);


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