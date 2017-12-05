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

        self.getCate(page,index)

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
        print(data['body'])
        if (data['isSuccess']):
            if (data['body'] is not None):
                body = json.loads(data['body'])
                print(body)
                del data
                if (index >= len(body) - 1):
                    index = len(body) - 1
                for index in range(index, len(body)):
                    self.listHandleData(page, body[index]['pagesize'], body[index]['id'], body[index]['psId'],
                                        body[index]['sceneId'])

    def listHandleData(self, page, pageSize, cateId, psId, sceneId):
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
        logUtils.info("列表 cateId:" + str(cateId) + "-->page:" + str(page) + "-->" + data['body'] + "-->" + dict['url'])
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)

                del jsonStr
                # print(body)
                if (body is not None):
                    #logUtils.info(page, ":", body)
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        # itemList = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre'];
                        del data
                        itemList = self.parserListItem(body)
                        del body
                        effectiveContentId = self.checkEffectiveContentId(itemList, cateId, page)
                        print("itemList size:", len(itemList))
                        print("effectiveContentId size:", len(effectiveContentId))
                        print("列表json:", itemList)
                        del itemList

                        if (effectiveContentId is not None and effectiveContentId['list'] is not None):
                            for index in range(len(effectiveContentId['list'])):
                                contentId = effectiveContentId['list'][index]
                                itemData = self.itemHandleData(contentId)
                                if (itemData is not None):
                                    dict = {'data': itemData,
                                            'cateId': cateId,
                                            'contentId': contentId,
                                            }
                                    if ('title' in itemData and itemData['title'] is not None):
                                        print("log baiduKeyWordsPos 111")
                                        # dict['keywords'] = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData(
                                        #    itemData['title'])
                                        print("log baiduKeyWordsPos 222")
                                    print("正在采集 size:", len(effectiveContentId['list']), " index:", index, " cate:",
                                          cateId,
                                          " page:", page, " contentId:", contentId)

                                    self.postItemData(dict)
                                del contentId
                                del itemData
                            if (effectiveContentId['isNextpage'] is not None and effectiveContentId[
                                'isNextpage'] is True):
                                del effectiveContentId
                                nextPage = page + 1;
                                self.getListData(cateId, dict, nextPage, pageSize, psId, sceneId)
                            else:
                                del effectiveContentId
                                pass
                        elif (effectiveContentId['isNextpage'] is not None and effectiveContentId[
                            'isNextpage'] is True):
                            nextPage = page + 1;
                            self.getListData(cateId, dict, nextPage, pageSize, psId, sceneId)
                        else:
                            pass;


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
        print("log reLoadList")
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
        del cookiesDict
        del url
        return self.getItemData(dict, contentId)


    def getItemData(self, dict, contentId):

        data = utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)
                del jsonStr
                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        del data
                        if ('data' in body and body['data'] is not None and
                                    'models' in body['data'] and body['data']['models'] is not None
                            and 'content' in body['data']['models']
                            and body['data']['models']['content'] is not None
                            ):
                            content = body['data']['models']['content']
                            del body
                            return content;
                        else:
                            return None
                    elif (dict['reLoadList']):
                        return self.reLoadItem(data, dict, contentId);
                    else:
                        del data
                        return None;
                else:
                    return self.reLoadItem(data, dict, contentId);
            else:
                return self.reLoadItem(data, dict, contentId);
        else:
            return self.reLoadItem(data, dict, contentId);


    def reLoadItem(self, data, dict, contentId):
        print("log reLoadItem")
        dict['isCookie'] = True;
        # print(str(type(data)), str(type(['get_cookie'])))
        if (data is not None and 'get_cookie' in data and data['get_cookie'] is not None and '_m_h5_tk' in data[
            'get_cookie']):
            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
            if (dict['reLoadList']):
                dict['url'] = self.getItemUrl(cookieArr[0], contentId);
                dict['putCookie'] = cookie
                dict['reLoadList'] = False
                del cookieArr
                del cookie
                del data
                return self.getItemData(dict, contentId);
            else:
                del cookieArr
                del cookie
                del data
                return None;
        else:
            del data
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

    def checkEffectiveContentId(self, dict, cateId, page):

        contentIdList = [];
        if (dict is not None and len(dict) > 0):
            for index in range(len(dict)):
                contentId = int(dict[index]['contentId'])
                contentIdList.append(contentId)
            del dict
            if (len(contentIdList) > 0):
                dataDict = {
                    'data': contentIdList,
                    'cateId': cateId,
                    'page': page,
                }
                postDict = {
                    'data': json.dumps(dataDict),
                }
                del dataDict
                dict = {
                    'url': config.config.checkEffectiveContentIdList,
                    'requestType': 'POST',
                    'isProxy': False,
                    'isHttps': False,
                    'postData': postDict,
                    'reLoad': True,
                }

                del postDict
                data = utils.netUtils.netUtils.getData(dict)

                del dict
                if (data["isSuccess"] and data["body"] is not None):
                    body = json.loads(data["body"])
                    del data

                    ret = [item for item in contentIdList if item not in body['data']]
                    dictData = {
                        'list': ret,
                        'isNextpage': body['isNextpage'],
                    }
                    del ret
                    del body
                    # os._exit(0)
                    return dictData
                else:
                    del data
        dictData = {
            'list': contentIdList,
            'isNextpage': False,
        }
        return contentIdList

    def postItemData(self,dict):

        postDict = {
            'data': json.dumps(dict),
        }
        del dict
        dict = {
            'url': config.config.addbuyInventoryItemData,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        del postDict
        data = utils.netUtils.netUtils.getData(dict)
        del dict
        if (data['isSuccess']):
            # logUtils.info("提交服务器成功", data)
            pass
        else:
            # logUtils.info("提交服务器失败", data)
            pass
        del data
        #logUtils.info("----")
