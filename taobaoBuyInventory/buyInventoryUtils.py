import taobaoBuyInventory.config
import time
import utils.netUtils
import config.config as appConfig
import json
import config.config
from taobaoBuyInventory.logUtils import logUtils


class buyInventoryUtils:
    def getData(self, page=1, index=0):
        # return self.listHandleData(page, tabId);
        self.getCate(page,index)

    def getCate(self, page=1, index=0):
        dict = {
            'url': config.config.getBuyinventoryCate,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
        }
        data = utils.netUtils.netUtils.getData(dict)
        if (data['isSuccess']):
            if (data['body'] is not None):
                body = json.loads(data['body'])
                if (index >= len(body) - 1):
                    index = len(body) - 1
                for index in range(index, len(body)):
                    self.listHandleData(page, body[index]['psId'], body[index]['sceneId'])


    def listHandleData(self, page, psId, sceneId):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getListUrl(cookiesDict['cookies'], page, psId, sceneId);
        logUtils.info("list url:", url)
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }

        return self.getListData(dict, page, psId, sceneId);

    def getListData(self, dict, page, psId, sceneId):
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)
                # print(body)
                if (body is not None):
                    logUtils.info(page, ":", body)
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        # itemList = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre'];
                        itemList = self.parserListItem(body)
                        # print(itemList)
                        effectiveContentId=self.checkEffectiveContentId(itemList)
                        #print("effectiveContentId:",effectiveContentId)
                        if (effectiveContentId is not None):
                            for index in range(len(effectiveContentId)):
                                contentId = effectiveContentId[index]
                                itemData = self.itemHandleData(contentId)
                                dict={'data':itemData,
                                      'contentId':contentId,
                                      }
                                self.postItemData(dict)

                        return body;

                    elif (dict['reLoadList']):
                        return self.reLoadList(data, dict, page, psId, sceneId);
                    else:
                        return None;
                else:
                    return self.reLoadList(data, dict, page, psId, sceneId);
            else:
                return self.reLoadList(data, dict, page, psId, sceneId);
        else:
            return self.reLoadList(data, dict, page, psId, sceneId);


    def parserListItem(self, body):
        #body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre']
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
                return body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre']
            elif ('qdList' in body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]):
                return body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['qdList']
            else:
                return None
        else:
            return None;


    def reLoadList(self, data, dict, page, psId, sceneId):
        dict['isCookie'] = True;
        if ('_m_h5_tk' in data['get_cookie']):
            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
            if (dict['reLoadList']):
                dict['url'] = self.getListUrl(cookieArr[0], page, psId, sceneId);
                dict['putCookie'] = cookie
                dict['reLoadList'] = False
                return self.getListData(dict, page, psId, sceneId);
            else:
                return None;
        else:
            return None


    def getListUrl(self, cookie, page, psId, sceneId):
        if (cookie is None):
            cookie = "";
        dataStr = str(taobaoBuyInventory.config.buyInventoryListData)
        topic = str(psId) + "_" + str(sceneId)
        data = dataStr % (
            page, topic, taobaoBuyInventory.config.listPageSize, psId, page, "" if sceneId == 0 else sceneId)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoBuyInventory.config.buyInventoryListUrl.format(appConfig.appkey, times, sign, data)
        # print(url)
        return url


    def itemHandleData(self, contentId):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getItemUrl(cookiesDict['cookies'], contentId);

        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }
        return self.getItemData(dict, contentId)


    def getItemData(self, dict, contentId):

        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)

                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        if (body['data'] is not None and body['data']['models'] is not None):
                            return body['data']['models'];
                        else:
                            return None
                    elif (dict['reLoadList']):
                        return self.reLoadItem(data, dict, contentId);
                    else:
                        return None;
                else:
                    return self.reLoadItem(data, dict, contentId);
            else:
                return self.reLoadItem(data, dict, contentId);
        else:
            return self.reLoadItem(data, dict, contentId);


    def reLoadItem(self, data, dict, contentId):
        dict['isCookie'] = True;
        # print(str(type(data)), str(type(['get_cookie'])))
        if (data is not None and 'get_cookie' in data and data['get_cookie'] is not None and '_m_h5_tk' in data[
            'get_cookie']):
            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
            if (dict['reLoadList']):
                dict['url'] = self.getItemData(cookieArr[0], dict, contentId);
                dict['putCookie'] = cookie
                dict['reLoadList'] = False
                return self.getItemData(dict, dict, contentId);
            else:
                return None;
        else:
            return None


    def getItemUrl(self, cookie, contentId):
        if (cookie is None):
            cookie = "";
        data = taobaoBuyInventory.config.buyInventoryItemData.format(contentId)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoBuyInventory.config.buyInventoryItemUrl.format(appConfig.appkey, times, sign, data)
        # print(url)
        return url;


    def checkEffectiveContentId(self,dict):
        list = [];
        if (dict is not None and len(dict) > 0):
            for index in range(len(dict)):
                contentId = dict[index]['contentId']
                list.append(contentId)
            if (len(list) > 0):
                postDict = {
                    'data': json.dumps(list),
                }

                dict = {
                    'url': config.config.checkEffectiveContentIdList,
                    'requestType': 'POST',
                    'isProxy': False,
                    'isHttps': False,
                    'postData': postDict,
                    'reLoad': True,
                }
                data = utils.netUtils.netUtils.getData(dict)
                if (data["isSuccess"] and data["body"] is not None):
                    return json.loads(data["body"])

        return list

    def postItemData(self,dict):
        postDict = {
            'data': json.dumps(dict),
        }

        dict = {
            'url': config.config.addbuyInventoryItemData,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }

        data = utils.netUtils.netUtils.getData(dict)
        if (data['isSuccess']):
            logUtils.info("提交服务器成功")
        else:
            logUtils.info("提交服务器失败", data)
        logUtils.info("----")