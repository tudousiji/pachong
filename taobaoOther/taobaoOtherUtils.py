# from utils.logUtils import logUtils as baseLogUtils
# import sys
import gc
import json

import config.config
import taobaoOther.askEveryBody
import taobaoOther.baiduKeyWordsPos
import taobaoOther.comment
import taobaoOther.reason
import utils.netUtils
from taobaoOther.logUtils import logUtils


class taobaoOtherUtils:
    def getData(self):
        dict = {
            'url': config.config.getTaoBaoItemInfoList,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        self.getItemDataWhile(dict);

    def getItemDataWhile(self, dataDict):
        while (True):
            data = utils.netUtils.netUtils.getData(dataDict);
            if (data['isSuccess']):
                if (data['body'] is not None):
                    body = json.loads(data['body'])
                    if (len(body) > 0):
                        self.getItemData(body)
                    else:
                        del dataDict
                        del body
                        del data
                        logUtils.info("已结束")
                else:
                    break
                    del dataDict
                    del data
                    logUtils.info("已结束,可能出错")
            else:
                break
                del dataDict
                del data
                logUtils.info("已结束,可能出错")

    def getItemData(self, body):
        if (len(body) > 0):
            list = [];
            for item in body:
                logUtils.info("开始itemId:", item['itemId'])
                dictData = {}
                keywordsDict = {}
                if (item["keywords"]['status']):
                    keywordsObj = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos()
                    keywordsData = keywordsObj.getData(
                        item["keywords"]['title'])
                    if (keywordsData is not None and keywordsData != 'null'):
                        keywordsDict['status'] = item["keywords"]['status']
                        keywordsDict['data'] = keywordsData
                    else:
                        keywordsDict['status'] = False;
                    del keywordsData
                    del keywordsObj
                else:
                    keywordsDict['status'] = False;

                dictData['keywords'] = keywordsDict
                del keywordsDict
                logUtils.info("结束关键词itemId:", item['itemId'])
                reasonDict = {}

                if (item["reason"]):
                    reasonObj = taobaoOther.reason.reason()
                    reasonData = reasonObj.getData(item['itemId'])

                    if (reasonData is not None and reasonData != 'null'):
                        reasonDict['status'] = item["reason"]
                        reasonDict['data'] = reasonData
                    else:
                        reasonDict['status'] = False;
                    del reasonData
                    del reasonObj
                else:
                    reasonDict['status'] = False;
                dictData['reason'] = reasonDict
                del reasonDict
                logUtils.info("结束理由itemId:", item['itemId'])
                commentDict = {}
                if (item["commentList"]):
                    commentObj = taobaoOther.comment.comment()
                    commentData = commentObj.getData(item['itemId'], 1)
                    if (commentData is not None and commentData != 'null'):
                        commentDict['status'] = item["commentList"]
                        commentDict['data'] = commentData
                    else:
                        commentDict['status'] = False;
                    del commentData
                    del commentObj
                else:
                    commentDict['status'] = False;
                dictData['commentList'] = commentDict
                del commentDict
                logUtils.info("结束评论itemId:", item['itemId'])
                askeverybodyListDict = {}
                if (item["askeverybodyList"]):
                    askeverybodyObj = taobaoOther.askEveryBody.askEveryBody()
                    askeverybodyData = askeverybodyObj.getData(item['itemId'])
                    if (askeverybodyData is not None and askeverybodyData != 'null'):
                        askeverybodyListDict['status'] = item["askeverybodyList"]
                        askeverybodyListDict['data'] = askeverybodyData
                    else:
                        askeverybodyListDict['status'] = False;
                    del askeverybodyData
                    del askeverybodyObj
                else:
                    askeverybodyListDict['status'] = False;
                dictData['askeverybodyList'] = askeverybodyListDict
                del askeverybodyListDict
                logUtils.info("结束问大家itemId:", item['itemId'])

                dictData['itemId'] = item['itemId'];
                logUtils.info(dictData)
                list.append(dictData);
                del dictData
                # baseLogUtils.info("baseLogUtils", "1")

            gc.collect()
            self.postData(list, dict);

    def postData(self, lists, dictList):
        postDict = {
            'data': json.dumps(lists),
        }
        del lists
        dict = {
            'url': config.config.addTaoBaoItemInfo,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        del postDict
        data = utils.netUtils.netUtils.getData(dict)

        if (data['isSuccess']):
            logUtils.info("提交服务器成功")
        else:
            logUtils.info("提交服务器失败", data)
        del dict
        del data
        gc.collect()
        # self.getItemData(dictList);
        logUtils.info("----")
