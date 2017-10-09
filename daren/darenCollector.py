import utils.netUtils
import daren.config
import utils.utils
import json
import config.config

class darenCollector:
    def getDarenList(self):
        for index in range(1,2):
            self.getData(index)

    def getData(self,index):
        #print(index)
        #return
        headers = {
            "Referer": "https://v.taobao.com/v/daren/find",
        }
        dict1 = {
            'url': daren.config.darenListUrl.format(index),
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'reLoad': True,
            'header':headers,
        }
        dataJson =utils.utils.utils.replacePreGetBody(utils.netUtils.netUtils.getData(dict1)['body'],'jsonp102(') ;
        data=json.loads(dataJson)
        if(type(data['data']) == dict and type(data['data']['result']) == list and len(data['data']['result'])>0 ):
            postDict = {
                'data': json.dumps(data['data']['result']),
            }
            dict2 = {
                'url': config.config.addDarenUrl,
                'requestType': 'POST',
                'isProxy': False,
                'isHttps': False,
                'postData': postDict,
                'reLoad': True,
            }
            data = utils.netUtils.netUtils.getData(dict2)
            print(data)
