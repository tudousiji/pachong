import config.config
import utils.netUtils
import json
import taobaoOther.baiduKeyWordsPos
import taobaoOther.comment
import taobaoOther.reason
import taobaoOther.askEveryBody
from taobaoOther.logUtils import logUtils
# from utils.logUtils import logUtils as baseLogUtils
# import sys
import gc

class taobaoOtherUtils:
    def getData(self):
        dict = {
            'url': config.config.getTaoBaoItemInfoList,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        self.getItemData(dict);


    def getItemData(self,dict):
        data= utils.netUtils.netUtils.getData(dict);

        if (data['isSuccess']):
            if (data['body'] is not None):
                body = json.loads(data['body'])
                if(len(body)>0):
                    list=[];
                    del data
                    for item in body:

                        logUtils.info("开始itemId:",item['itemId'])
                        dictData={}
                        keywordsDict={}
                        if(item["keywords"]['status']):
                            keywordsData = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData(
                                item["keywords"]['title'])
                            if (keywordsData is not None and keywordsData != 'null'):
                                keywordsDict['status'] =item["keywords"]['status']
                                keywordsDict['data'] = keywordsData
                            else:
                                keywordsDict['status'] = False;
                            del keywordsData
                        else:
                            keywordsDict['status'] = False;

                        dictData['keywords']=keywordsDict
                        del keywordsDict
                        logUtils.info("结束关键词itemId:", item['itemId'])
                        reasonDict = {}

                        if (item["reason"]):
                            reasonData = taobaoOther.reason.reason().getData(item['itemId'])

                            if (reasonData is not None and reasonData != 'null'):
                                reasonDict['status'] = item["reason"]
                                reasonDict['data'] = reasonData
                            else:
                                reasonDict['status'] = False;
                            del reasonData
                        else:
                            reasonDict['status'] = False;
                        dictData['reason'] = reasonDict
                        del reasonDict
                        logUtils.info("结束理由itemId:", item['itemId'])
                        commentDict = {}
                        if (item["commentList"]):
                            commentData = taobaoOther.comment.comment().getData(item['itemId'], 1)
                            if (commentData is not None and commentData != 'null'):
                                commentDict['status'] = item["commentList"]
                                commentDict['data'] = commentData
                            else:
                                commentDict['status'] = False;
                            del commentData
                        else:
                            commentDict['status'] = False;
                        dictData['commentList'] = commentDict
                        del commentDict
                        logUtils.info("结束评论itemId:", item['itemId'])
                        askeverybodyListDict = {}
                        if (item["askeverybodyList"]):
                            askeverybodyData = taobaoOther.askEveryBody.askEveryBody().getData(item['itemId'])
                            if (askeverybodyData is not None and askeverybodyData != 'null'):
                                askeverybodyListDict['status'] = item["askeverybodyList"]
                                askeverybodyListDict['data'] = askeverybodyData
                            else:
                                askeverybodyListDict['status'] = False;
                            del askeverybodyData
                        else:
                            askeverybodyListDict['status'] = False;
                        dictData['askeverybodyList'] = askeverybodyListDict
                        del askeverybodyListDict
                        logUtils.info("结束问大家itemId:", item['itemId'])

                        dictData['itemId']=item['itemId'];
                        logUtils.info(dictData)
                        list.append(dictData);
                        del dictData
                        # baseLogUtils.info("baseLogUtils", "1")
                    del body

                    gc.collect()
                    self.postData(list);
                    self.getItemData(dict);
                else:
                    del body
                    logUtils.info("已结束")
            else:
                del dict
                del data
        else:
            del dict



    def postData(self,lists):
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
        logUtils.info("----")


