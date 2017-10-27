import taobaoOther.config
import utils.netUtils
import utils.utils
import json


class baiduKeyWordsPos:

    maxKeyWordsCount=5;
    def getData(self,keyword):
        dict = {
            'url': taobaoOther.config.baiduKeyWordsPos.format(keyword),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
        }
        return self.getItemData(dict)

    def getItemData(self,dict):
        data = utils.netUtils.netUtils.getData(dict);
        if(data['isSuccess']):
            if (data['body'] is not None):
                body=json.loads(data['body']);
                if('result' in body and "res" in body['result'] and "keyword_list" in body['result']['res']):

                    if(len(body['result']['res']['keyword_list'])>=baiduKeyWordsPos.maxKeyWordsCount):
                        return json.dumps(body['result']['res']['keyword_list'])
                    else:
                        keyWordsList=[];
                        keyWordsList.append(body['result']['res']['keyword_list'])
                        for item in body['result']['res']['wordrank'] :
                            print(item)
                else:
                    return None;
            else:
                return None
        else:
            return None;
