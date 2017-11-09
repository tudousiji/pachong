import taobaoBuyInventory.config
import time
import utils.netUtils
import config.config as appConfig
import json


class buyInventoryUtils:
    def getData(self, page, tabId):
        return self.listHandleData(page, tabId);

    def listHandleData(self, page, tabId):
        cookiesDict = utils.taobaokeUtils.taobaokeUtils.getCookies();
        url = self.getListUrl(cookiesDict['cookies'], page, tabId);
        print("list url:", url)
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoadList': True,
            'putCookie': cookiesDict['putCookie'],
            'isCookie': True,
        }

        return self.getListData(dict, page, tabId);

    def getListData(self, dict, page, tabId):
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)
                # print(body)
                if (body is not None):
                    print(body)
                    if (str(body['ret']).startswith("['FAIL_") is not True):
                        itemList = body['data']['result']['1891397']['result'][0]['data'][0]['data'][0][0]['pre'];
                        for index in range(len(itemList)):
                            contentId = itemList[index]['contentId']
                            # print("contentId:",contentId)
                            itemData = self.itemHandleData(contentId)
                            print(index, " ", contentId, ":", itemData)
                        itemData = self
                        # print(body)
                        return body;
                    elif (dict['reLoadList']):
                        return self.reLoadList(data, dict, page, tabId);
                    else:
                        return None;
                else:
                    return self.reLoadList(data, dict, page, tabId);
            else:
                return self.reLoadList(data, dict, page, tabId);
        else:
            return self.reLoadList(data, dict, page, tabId);

    def reLoadList(self, data, dict, page, tabId):
        dict['isCookie'] = True;
        if ('_m_h5_tk' in data['get_cookie']):
            cookieArr = data['get_cookie']['_m_h5_tk'].split('_')
            cookie = utils.taobaokeUtils.taobaokeUtils.putCookies(data['get_cookie']);
            if (dict['reLoadList']):
                dict['url'] = self.getListUrl(cookieArr[0], page, tabId);
                dict['putCookie'] = cookie
                dict['reLoadList'] = False
                return self.getListData(dict, page, tabId);
            else:
                return None;
        else:
            return None

    def getListUrl(self, cookie, page, tabId):
        if (cookie is None):
            cookie = "";
        dataStr = str(taobaoBuyInventory.config.buyInventoryListData)
        data = dataStr % (page, taobaoBuyInventory.config.listPageSzie, page)
        times = str(int(round(time.time() * 1000)));
        sign = utils.netUtils.netUtils.getTbkSign(cookie, appConfig.appkey, times, data)
        url = taobaoBuyInventory.config.buyInventoryListUrl.format(appConfig.appkey, times, sign, data)
        # print(url)
        return url;

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
        return self.getItemData(dict, contentId);

    def getItemData(self, dict, contentId):
        data = utils.netUtils.netUtils.getData(dict);
        if (data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], "mtopjsonp1(");
                body = json.loads(jsonStr)

                if (body is not None):
                    if (str(body['ret']).startswith("['FAIL_") is not True):

                        return body;
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
        print(str(type(data)), str(type(['get_cookie'])))
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
