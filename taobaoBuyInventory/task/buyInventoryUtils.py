import taobaoBuyInventory.config
import time
import utils.netUtils
import config.config as appConfig
import json
import config.config
from taobaoBuyInventory.logUtils import logUtils
import taobaoOther.baiduKeyWordsPos


class buyInventoryUtils:
    def getData(self, page=1, index=0):
        # return self.listHandleData(page, tabId);

        self.getCate(page, index)

    def getCate(self, page=1, index=0):

        dict = {
            'url': config.config.getBuyinventoryCate,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
        }
        print("url:", dict['url'])
        data = utils.netUtils.netUtils.getData(dict)
        del dict
        if (data['isSuccess']):
            if (data['body'] is not None):
                body = json.loads(data['body'])
                del data
                if (index >= len(body) - 1):
                    index = len(body) - 1
                for index in range(index, len(body)):
                    self.listHandleData(page, body[index]['pagesize'], body[index]['id'], body[index]['psId'],
                                        body[index]['sceneId'])

    def listHandleData(self, page, pageSize, cateId, psId, sceneId):
        print("id:", cateId, " page:", page)
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getListUrl(cookiesDict['cookies'], page, pageSize, psId, sceneId);
        # logUtils.info("list url:", url)
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }
        del cookiesDict
        del url
        self.getListData(cateId, dict, page, pageSize, psId, sceneId);

    def getListData(self, cateId, dict, page, pageSize, psId, sceneId):
        data = utils.netUtils.netUtils.getData(dict);
        print("getListData:", data)
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)

                del jsonStr
                # print(body)
                if (body is not None):
                    # logUtils.info(page, ":", body)
                    if ('ret' in body and str(body['ret']).startswith("['FAIL_") is not True):
                        # itemList = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre'];
                        del data
                        itemList = self.parserListItem(body)
                        if itemList is not None:
                            contentIdList = [];
                            for item in itemList:
                                contentIdList.append(item['contentId'])
                            postDict = {
                                'data': contentIdList,
                                'page': page,
                                'cateId': cateId,
                            }
                            self.postContentId(postDict, cateId, dict, page, pageSize, psId, sceneId)
                        else:
                            pass


                    elif (dict['reLoadList']):
                        self.reLoadList(data, cateId, dict, page, pageSize, psId, sceneId);
                    else:
                        del data
                        pass;
                else:
                    self.reLoadList(data, cateId, dict, page, pageSize, psId, sceneId);
            else:
                self.reLoadList(data, cateId, dict, page, pageSize, psId, sceneId);
        else:
            self.reLoadList(data, cateId, dict, page, pageSize, psId, sceneId);

    def postContentId(self, dataDict, cateId, dict, page, pageSize, psId, sceneId):
        postDict = {
            'data': json.dumps(dataDict),
        }

        # del dataDict
        contentIdDict = {
            'url': config.config.addContentId,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
            '': True,
        }

        del postDict
        data = utils.netUtils.netUtils.getData(contentIdDict)

        print(data)
        if (data["isSuccess"] and data["body"] is not None):
            body = json.loads(data["body"])
            print((body is not None and body["isNextpage"] is True))
            # logUtils.info("服务器提交成功")
            if body is not None and body["isNextpage"] is True:
                nextPage = page + 1;
                cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
                url = self.getListUrl(cookiesDict['cookies'], page, pageSize, psId, sceneId);
                dict['url'] = url;
                del cookiesDict;
                del url;
                self.getListData(cateId, dict, nextPage, pageSize, psId, sceneId)

        else:
            # logUtils.info("服务器提交失败:"+str(data))
            pass

    def parserListItem(self, body):

        # body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre']
        if (body is not None and 'data' in body and
                    body['data'] is not None and 'result' in body['data'] and
                    body['data']['result'] is not None and '1891397' in body['data']['result'] and
                    body['data']['result']['1891397'] is not None and 'result' in body['data']['result']['1891397'] and
                    body['data']['result']['1891397']['result'] is not None and len(
            body['data']['result']['1891397']['result']) > 0 and
                    'data' in body['data']['result']['1891397']['result'][0] and len(
            body['data']['result']['1891397']['result'][0]['data']) > 0 and
                    'data' in body['data']['result']['1891397']['result'][0]['data'][0] and len(
            body['data']['result']['1891397']['result'][0]['data'][0]['data']) > 0 and
                    len(body['data']['result']['1891397']['result'][0]['data'][0]['data'][0]) > 0
            ):
            if ('pre' in body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]):
                content = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre']
                del body
                return content
            elif ('qdList' in body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]):
                content = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['qdList']
                del body
                return content
            else:
                del body
                return None
        else:
            del body
            return None;

    def reLoadList(self, data, cateId, dict, page, pageSize, psId, sceneId):
        # print("log reLoadList")
        dict['isCookie'] = True;
        if (data is not None and data['get_cookie'] is not None and '_m_h5_tk' in data['get_cookie'] and
                    data['get_cookie']['_m_h5_tk'] is not None):
            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
            del data
            if (dict['reLoadList']):
                dict['url'] = self.getListUrl(cookieArr[0], page, pageSize, psId, sceneId);
                dict['putCookie'] = cookie
                dict['reLoadList'] = False
                del cookie
                del cookieArr
                self.getListData(cateId, dict, page, pageSize, psId, sceneId);
            else:
                del cookie
                del cookieArr
                return None;
        else:
            del data
            return None

    def getListUrl(self, cookie, page, pageSize, psId, sceneId):

        if (cookie is None):
            cookie = "";
        dataStr = str(taobaoBuyInventory.config.buyInventoryListData)
        topic = str(psId) + "_" + str(sceneId)
        data = dataStr % (
            page, topic, pageSize, psId, page, "" if sceneId == 0 else sceneId)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoBuyInventory.config.buyInventoryListUrl.format(appConfig.appkey, times, sign, data)
        # print(url)
        del dataStr
        del topic
        del data
        del times
        del sign
        return url
