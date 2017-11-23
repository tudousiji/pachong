import taobaoOther.config
import utils.netUtils
import utils.utils
import json
from taobaoOther.logUtils import logUtils
import gc
class reason:
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
                del data
                body = json.loads(jsonStr);
                del jsonStr
                if(body['data'] is not None and len(body['data']['impress'])>0):
                    content = json.dumps(body['data'])
                    del body
                    gc.collect()
                    return content;
                else:
                    del body
                    gc.collect()
                    return self.getItemDataReLoad(dict);
            else:
                del data
                return None
        else:
            del data
            return self.getItemDataReLoad(dict);

    # 单条内容获取失败重试
    def getItemDataReLoad(self, dict):
        # print(cookieArr[0])
        gc.collect()
        if (dict['reLoad']):
            dict['reLoad'] = False
            return self.getItemData(dict);
        else:
            return None;
