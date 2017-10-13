import utils.netUtils as netUtils
import json


class utils:
    @staticmethod
    def replacePreGetBody(body,replace):
        if(body.find(replace)>=0):
            body=body.strip();
            #print(body[len(body)-2])
            #print(len(body))
            if(body.rfind(';')==len(body)-1):
                #print("是;")
                body = body[body.index(replace) + len(replace):len(body) - 2];
            elif (body.rfind(')')==len(body)-1):
                #print("是)")
                body = body[body.index(replace) + len(replace):len(body) - 1];
        return body;


    @staticmethod
    def postDataForService(data,url):#data是字典等不是json字符
        postDict = {
            'data': json.dumps(data),
        }
        dict = {
            'url': url,
            'requestType': 'POST',
            'isProxy': False,
            'isHttps': False,
            'postData': postDict,
            'reLoad': True,
        }

        return netUtils.netUtils.getData(dict)
        #data = utils.netUtils.netUtils.getData(dict)
        #utils.netUtils.netUtils.getData(dict)
