import config.config as appConfig
import utils
import json
import taobaoBuyInventory.config
import time
import gc
import urllib
import sys

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
                            contentDict = self.itemHandleData(contentId)
                            if contentDict is not None:

                                postDict = {
                                    "data": contentDict['content'],
                                    "contentId": contentId,
                                    "cate_id": item["cateId"],
                                }
                                print("contentDict:::" + json.dumps(postDict))
                                self.postItemData(None, postDict)
                                del postDict

                                if ("personContent" in contentDict and contentDict['personContent'] is not None
                                    and len(contentDict['personContent']) > 0):
                                    personContentidList = [];
                                    for personItem in contentDict['personContent']:
                                        personContentidList.append(personItem['id'])
                                    if len(personContentidList) > 0:
                                        personContentDict = {
                                            "data": personContentidList,
                                            "contentId": contentId,
                                            "cateId": item["cateId"],
                                            "page": item["page"],
                                        }
                                        self.postPersonContentData(None, personContentDict)
                                        del personContentDict
                                    del personContentidList

                                if ("tags" in contentDict and contentDict['tags'] is not None
                                    and len(contentDict['tags']) > 0):
                                    tagsList = [];
                                    for tagItem in contentDict['tags']:
                                        tagItemUrl = urllib.parse.urlparse(tagItem['url'])
                                        tagItemParse_qs = urllib.parse.parse_qs(tagItemUrl.query, True)
                                        if tagItemParse_qs is not None and 'tag' in tagItemParse_qs and tagItemParse_qs[
                                            'tag'] is not None and len(tagItemParse_qs['tag']) > 0:
                                            tagsList.append(tagItemParse_qs['tag'][0])
                                        del tagItemUrl
                                        del tagItemParse_qs
                                    if len(tagsList) > 0:
                                        tagsDict = {
                                            "data": tagsList,
                                            "contentId": contentId,
                                            "cateId": item["cateId"],
                                            "page": item["page"],
                                        }
                                        self.postTagsData(None, tagsDict)
                                        del tagsDict
                                    del tagsList


                            del contentId
                            del contentDict
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

                            ):
                            contentDict = {}
                            if ('content' in body['data']['models'] and body['data']['models']['content'] is not None):
                                # content = body['data']['models']['content']
                                content = {};
                                content["title"] = body['data']['models']['content']['title']
                                content["subTitle"] = body['data']['models']['content']['subTitle']
                                content["summary"] = body['data']['models']['content']['summary']
                                content["gmtCreate"] = body['data']['models']['content']['gmtCreate']
                                content["readCount"] = body['data']['models']['content']['readCount']

                                if 'richText' in body['data']['models']['content'] and len(
                                        body['data']['models']['content']['richText']) > 0:
                                    content["richText"] = body['data']['models']['content']['richText'];
                                elif 'modules' in body['data'] and body['data']['modules'] is not None:
                                    itemList = [];
                                    for item in body['data']['modules']:
                                        if "data" in item and item["data"] is not None:
                                            if "title" in item["data"] and item["data"][
                                                "title"] is not None and "topNum" in item["data"] and item["data"][
                                                "topNum"] is not None:
                                                titleDict = {
                                                    "title": item["data"]
                                                }
                                                # del titleDict["title"]["items"]

                                                if "items" in item["data"] and item["data"][
                                                    "items"] is not None and len(item["data"]["items"]) > 0:
                                                    itemsItemList = self.__itemsItemList(item["data"]["items"]);
                                                    # del titleDict["title"]["items"]

                                                    if itemsItemList is not None and len(itemsItemList) > 0:
                                                        titleDict["title"]["items"] = itemsItemList
                                                    del itemsItemList
                                                itemList.append(titleDict)
                                                del titleDict
                                            elif "shopDetail" in item["data"] and item["data"][
                                                "shopDetail"] is not None:
                                                shopDetailList = [];
                                                for shopDetailItem in item["data"]["shopDetail"]:
                                                    shopDetailDict = {
                                                        "description": shopDetailItem["description"],
                                                        "shop_img": shopDetailItem["shop_img"],
                                                        "shop_logo": shopDetailItem["shop_logo"],
                                                        "title": shopDetailItem["title"],
                                                        "shop_title": shopDetailItem["shop_title"],
                                                        "shop_url": shopDetailItem["shop_url"],
                                                        "linkUrl": shopDetailItem["linkUrl"],
                                                        "id": shopDetailItem["id"],
                                                        "level": shopDetailItem["level"],
                                                        "shop_desc ": shopDetailItem["shop_desc"],
                                                        "shop_sid ": shopDetailItem["shop_sid"],
                                                        "b2cShop ": shopDetailItem["b2cShop"],
                                                        "type ": shopDetailItem["type"],
                                                    }
                                                    shopDetailList.append(shopDetailDict)
                                                if (len(shopDetailList) > 0):
                                                    shopDetailListDict = {
                                                        "shopDetail": shopDetailList
                                                    }
                                                    itemList.append(shopDetailListDict)
                                                del shopDetailList
                                                del shopDetailListDict
                                            elif "images" in item["data"] and item["data"]["images"] is not None:
                                                shopDetailListDict = {
                                                    "images": item["data"]["images"]
                                                }
                                                itemList.append(shopDetailListDict)
                                                del shopDetailListDict
                                            elif "text" in item["data"] and item["data"]["text"] is not None and len(
                                                    item["data"]["text"]) == 1:
                                                shopDetailListDict = {
                                                    "text": item["data"]["text"]
                                                }
                                                itemList.append(shopDetailListDict)
                                            elif "items" in item["data"] and item["data"]["items"] is not None:
                                                itemsItemList = self.__itemsItemList(item["data"]["items"]);
                                                if (itemsItemList is not None and len(itemsItemList) > 0):
                                                    itemsListDict = {
                                                        "items": itemsItemList
                                                    }
                                                    itemList.append(itemsListDict)
                                                    del itemsListDict
                                                del itemsItemList
                                    if len(itemList) > 0:
                                        content["modules"] = itemList
                                    del itemList
                                contentDict['content'] = content
                                del content
                            if 'personContent' in body['data']['models'] and body['data']['models'][
                                'personContent'] is not None:
                                personContent = body['data']['models']['personContent']
                                contentDict['personContent'] = personContent
                                del personContent
                            if 'tags' in body['data']['models'] and body['data']['models']['tags'] is not None:
                                tagsList = body['data']['models']['tags']
                                contentDict['tags'] = tagsList
                                del tagsList
                            del body
                            gc.collect()
                            return contentDict;

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

    def __itemsItemList(self, items):

        if items is not None and len(items) > 0:
            itemsItemList = [];
            for itemsItem in items:
                itemsItemDict = {
                    "itemType": itemsItem["itemType"],
                    "itemTitle": itemsItem["itemTitle"],
                    "itemClickNativeUrl": itemsItem["itemClickNativeUrl"],
                    "itemId": itemsItem["itemId"],
                    "itemQualityDTO": itemsItem["itemQualityDTO"],
                    "item_pic": itemsItem["item_pic"],
                    "itemUrl": itemsItem["itemUrl"],
                    "itemPriceDTO": itemsItem["itemPriceDTO"],
                }

                itemsItemList.append(itemsItemDict)
            return itemsItemList
        else:
            return None;

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

    def postTagsData(self, tagsDict, tagsDataDict):
        if tagsDict is None:
            postDict = {
                'data': json.dumps(tagsDataDict),
            }
            # print("postTagsData:"+json.dumps(tagsDataDict))
            # del dataDict
            tagsDict = {
                'url': appConfig.addBuyinventoryTags,
                'requestType': 'POST',
                'isProxy': False,
                'isHttps': False,
                'postData': postDict,
                'reLoadCount': 0,

            }
            # print("url:::"+tagsDict['url'])
            del postDict

        data = utils.netUtils.netUtils.getData(tagsDict)
        # print("postTagsData:"+str(data))
        if (data["isSuccess"] and data["body"] is not None):
            del tagsDataDict
            del tagsDict
            print("postTagsData服务器提交成功")
        elif (tagsDict['reLoadCount'] <= 20):
            print("postTagsData服务器提交失败，重试中.." + str(tagsDict['reLoadCount']))
            tagsDict['reLoadCount'] = tagsDict['reLoadCount'] + 1;

            self.postTagsData(tagsDict, tagsDataDict)
        else:
            print("postTagsData服务器提交失败:" + str(tagsDict['reLoadCount']) + "次")
            del tagsDataDict
            del tagsDict

    def postPersonContentData(self, contentIdDict, dataDict):
        if contentIdDict is None:
            postDict = {
                'data': json.dumps(dataDict),
            }
            # del dataDict
            contentIdDict = {
                'url': appConfig.addContentId,
                'requestType': 'POST',
                'isProxy': False,
                'isHttps': False,
                'postData': postDict,
                'reLoadCount': 0,

            }

        del postDict
        data = utils.netUtils.netUtils.getData(contentIdDict)

        print("postPersonContentData:" + str(data))
        if (data["isSuccess"] and data["body"] is not None):
            del contentIdDict
            del dataDict
            print("postPersonContentData服务器提交成功")
        elif (contentIdDict['reLoadCount'] <= 20):
            print("postPersonContentData服务器提交失败，重试中.." + str(contentIdDict['reLoadCount']))
            contentIdDict['reLoadCount'] = contentIdDict['reLoadCount'] + 1;
            self.postPersonContentData(contentIdDict, dataDict)
        else:
            print("postPersonContentData服务器提交失败:" + str(contentIdDict['reLoadCount']) + "次")
            del contentIdDict
            del dataDict

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

        if (data['isSuccess']):
            del dict
            print("提交服务器成功", data)
            # logUtils.info("提交服务器成功", data)
            pass
        elif dict['reLoadCount'] <= 20:
            print("提交服务器失败", data)
            time.sleep(dict['reLoadCount'] * 10)
            dict['reLoadCount'] = dict['reLoadCount'] + 1
            self.postData(self, dict, dictData)
            del dict
            # logUtils.info("提交服务器失败", data)
            pass
        else:
            del dict
            print("提交服务器失败,失败次数:" + dict['reLoadCount'], data)
        del data
        # logUtils.info("----")
