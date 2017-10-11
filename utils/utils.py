import utils.netUtils
import json
class utils:
    @staticmethod
    def replacePreGetBody(body,replace):
        if(body.find(replace)>=0):
            body=body.strip();
            #print(body[len(body)-2])
            #print(len(body))
            if(body.rfind(';')>=0):
                body = body[body.index(replace) + len(replace):len(body) - 2];
            else:
                body = body[body.index(replace) + len(replace):len(body) - 1];
        return body;


    @staticmethod
    def postDataForService(data,url):#data是字典等不是json字符
        postDict = {
            'data': json.dumps(dict),
        }
        dict = {
            'url': url,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }
        data = utils.netUtils.netUtils.getData(dict)
        utils.netUtils.netUtils.getData(dict)
