import utils.netUtils
import daren.config
import utils.utils
import json
import config.config
import time
import utils.taobaokeUtils
import os

class darenCollector:
    # 获取所有达人(5000条)
    def getDarenList(self):
        for index in range(1,11):
            self.getData(index)


    def getData(self,index):
        #print(index)
        #return
        headers = {
            "Referer": "https://v.taobao.com/v/daren/find",
        }
        dict1 = {
            'url': daren.config.darenListUrl.format(index),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'header':headers,
        }
        dataJson =utils.utils.utils.replacePreGetBody(utils.netUtils.netUtils.getData(dict1)['body'],'jsonp102(') ;
        data=json.loads(dataJson)
        if(type(data['data']) == dict and type(data['data']['result']) == list and len(data['data']['result'])>0 ):
            postDict = {
                'data': json.dumps(data['data']['result']),
            }
            dict2 = {
                'url': config.config.addDarenUrl,
                'requestType': 'POST',
                'isProxy': False,
                'isHttps': False,
                'postData': postDict,
                'reLoad': True,
            }
            data2 = utils.netUtils.netUtils.getData(dict2)



    def getDaRenHomeUrl(self,id=0):
        dict1 = {
            'url': config.config.getDaRenHomeUrl,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'id':id,
        }
        data = utils.netUtils.netUtils.getData(dict1)
        data=json.loads(data['body'])
        #print(data['data']['userId'])
        self.getDaRenHomeList(None,1,data['data']['userId']);

    def getDaRenHomeList(self,dict1,page,accountId):
        cookiesDict=utils.taobaokeUtils.taobaokeUtils.getCookies();
        url=self.getUrl(cookiesDict['cookies'],page,accountId);
        #print(cookiesDict)
        if(dict1 is None):
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                #'Referer': 'https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=639030980&userId=639030980',
                'Cookie': 'isg=Au7uNWIeOwV04U8sG5fjQPCePkdwR61AFRzkjBi3WvGs-45VgH8C-ZT5xV3o; t=5c1bcd6b227a98843f3e54fdff4906f0; cna=6dVHEs+q/RICAXL1IsROXyQK; thw=cn; um=70CF403AFFD707DF70B2F2FB37F0BAB5F98885A53E8D0C8D271255914AE269C79A6C7FBAF3F12998CD43AD3E795C914CAC077E3A127266F08C97FE37B93BF66D; l=Am1tPIeiS6/pzbzfIYPAe4jufQLna6Gc; ali_apache_id=11.131.227.29.1507604092438.267561.1; cookie2=1c794284bae91d3e63e3da81dff17ce7; v=0; _tb_token_=eb5613436af4; _m_h5_tk=39a026d06631864d2b39a99ac51db93a_1507624902590; _m_h5_tk_enc=3b9c275e42eb902de1fc2ca7786948ef',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Pragma': 'no-cache',
            }
            dict1 = {
                'url': url,
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoad': True,
                'putCookie':cookiesDict['putCookie'],
                'isCookie':True,
                'header': headers,
            }

        data = utils.netUtils.netUtils.getData(dict1)
        #print(data)
        if (data['isSuccess']):
            if (data['body'] is not None):
                #jsonStr = data['body'][data['body'].index('mtopjsonp8(') + len('mtopjsonp8('):len(data['body']) - 1];
                jsonStr=utils.utils.utils.replacePreGetBody(data['body'],"mtopjsonp5(");
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
                        dict1['isCookie'] = True;
                        cookieArr = data['get_cookie']['_m_h5_tk'].split('_')

                        cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
                        #print(cookieArr[0])
                        if(dict1['reLoad']):
                            dict1['url'] = self.getUrl(cookieArr[0],page,accountId);
                            dict1['putCookie'] = cookie
                            dict1['reLoad']=False
                            self.getDaRenHomeList(dict1, page, accountId);
                        pass



    def getUrl(self,cookie,page,accountId):
        if(cookie is None):
            cookie = "";
        times = str(int(round(time.time() * 1000)));
        data = daren.config.darenHomeListData.format(page, accountId)
        sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
        url = daren.config.darenHomeList.format(config.config.appkey, times, sign, data)

        return url;