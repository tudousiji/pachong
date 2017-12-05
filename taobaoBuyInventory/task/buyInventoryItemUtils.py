import config.config as appConfig
import utils
import json
import taobaoBuyInventory.config
import time


class buyInventoryItemUtils:
    def getData(self):
        while True:
            dict = {
                'url': appConfig.getContentIdList,
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': False,
                'reLoadList': True,
            }
            # print("url:", dict['url'])
            data = utils.netUtils.netUtils.getData(dict)
            if data['isSuccess']:
                if (data['body'] is not None):
                    body = json.loads(data['body'])
                    print("body:" + str(body))
                    if len(body) > 0:
                        for item in body:
                            contentId = item["contentId"]
                            content = self.itemHandleData(contentId)
                            postDict = {
                                "data": content,
                                "contentId": contentId,
                                "cate_id": item["cateId"],
                            }
                            self.postItemData(None, postDict)
                            del contentId
                            del content
                    else:
                        break
                else:
                    break
            else:
                break

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
        print("getItemData:" + str(contentId) + "-->" + str(data))
        print(dict['url'])
        print("--------")
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

    def postItemData(self, dict, dictData):
        if dict is None:
            postDict = {
                'data': json.dumps(dictData),
            }
            del dictData
            dict = {
                'url': appConfig.addbuyInventoryItemData,
                'requestType': 'POST',
                'isProxy': False,
                'isHttps': False,
                'postData': postDict,
                'reLoadCount': 0,
            }
        del postDict
        data = utils.netUtils.netUtils.getData(dict)
        del dict
        if (data['isSuccess']):
            print("提交服务器成功", data)
            # logUtils.info("提交服务器成功", data)
            pass
        elif dict['reLoadCount'] <= 20:
            print("提交服务器失败", data)
            time.sleep(dict['reLoadCount'] * 10)
            dict['reLoadCount'] = dict['reLoadCount'] + 1
            self.postData(self, dict, dictData)
            # logUtils.info("提交服务器失败", data)
            pass
        else:
            print("提交服务器失败,失败次数:" + dict['reLoadCount'], data)
        del data
        # logUtils.info("----")
