import config.config
import utils.netUtils
import json
import taobaoOther.baiduKeyWordsPos
import taobaoOther.comment
import taobaoOther.reason
import taobaoOther.askEveryBody
import sys


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
                    for item in body:
                        print("开始itemId:",item['itemId'])
                        dictData={}
                        keywordsDict={}
                        if(item["keywords"]['status']):
                            data = taobaoOther.baiduKeyWordsPos.baiduKeyWordsPos().getData(item["keywords"]['title'])
                            if(data is not None):
                                keywordsDict['status'] =item["keywords"]['status']
                                keywordsDict['data']=data
                            else:
                                keywordsDict['status'] = False;
                        else:
                            keywordsDict['status'] = False;

                        dictData['keywords']=keywordsDict
                        print("结束关键词itemId:", item['itemId'])
                        reasonDict = {}

                        if (item["reason"]):
                            data =taobaoOther.reason.reasin().getData(item['itemId'])

                            if (data is not None):
                                reasonDict['status'] = item["reason"]
                                reasonDict['data'] = data
                            else:
                                reasonDict['status'] = False;
                        else:
                            reasonDict['status'] = False;
                        dictData['reason'] = reasonDict
                        print("结束理由itemId:", item['itemId'])
                        commentDict = {}
                        if (item["commentList"]):
                            data=taobaoOther.comment.comment().getData(item['itemId'],1)
                            if (data is not None):
                                commentDict['status'] = item["commentList"]
                                commentDict['data'] = data
                            else:
                                commentDict['status'] = False;
                        else:
                            commentDict['status'] = False;
                        dictData['commentList'] = commentDict
                        print("结束评论itemId:", item['itemId'])
                        askeverybodyListDict = {}
                        if (item["askeverybodyList"]):
                            data=taobaoOther.askEveryBody.askEveryBody().getData(item['itemId'])
                            if (data is not None):
                                askeverybodyListDict['status'] = item["askeverybodyList"]
                                askeverybodyListDict['data'] = data
                            else:
                                askeverybodyListDict['status'] = False;
                        else:
                            askeverybodyListDict['status'] = False;
                        dictData['askeverybodyList'] = askeverybodyListDict
                        print("结束问大家itemId:", item['itemId'])

                        dictData['itemId']=item['itemId'];
                        print(dictData)
                        list.append(dictData);

                    self.postData(list);
                    self.getItemData(dict);
                else:
                    print("已结束")



    def postData(self,lists):
        postDict = {
            'data': json.dumps(lists),
        }
        dict = {
            'url': config.config.addTaoBaoItemInfo,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        data = utils.netUtils.netUtils.getData(dict)
        if (data['isSuccess']):
            print("提交服务器成功")
        else:
            print("提交服务器失败",data)
        print("----")