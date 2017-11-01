import taobaoOther.config
import utils.netUtils
import utils.utils
import json

class reasin:



    def getData(self,itemId):
        dict = {
            'url': taobaoOther.config.reasonUrl.format(itemId),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': True,
            'reLoad': True,
        }
        return self.getItemData(dict)

    def getItemData(self,dict):

        data=utils.netUtils.netUtils.getData(dict);
        if(data['isSuccess']):
            if (data['body'] is not None):
                jsonStr = utils.utils.utils.replacePreGetBody(data['body'], 'json_tbc_rate_summary(')
                body = json.loads(jsonStr);
                if(body['data'] is not None and len(body['data']['impress'])>0):
                    return json.dumps(body['data']);
                else:
                    return self.getItemDataReLoad(dict);
        else:
            return self.getItemDataReLoad(dict);

    # 单条内容获取失败重试
    def getItemDataReLoad(self, dict):
        # print(cookieArr[0])

        if (dict['reLoad']):
            dict['reLoad'] = False
            return self.getItemData(dict);
        else:
            return None;
