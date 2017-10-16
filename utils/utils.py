import utils.netUtils as netUtils
import json
import os
import requests
from pyexcel_xls import get_data

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


    @staticmethod
    def parseXls(url):
        r = requests.get(url)
        f = open("file_path.xls", "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        f.close();
        list = []
        xls_data = get_data(r"file_path.xls")


        list=[];
        for sheet_n in xls_data.keys():
            #print(sheet_n, ":", xls_data[sheet_n])
            list.append(xls_data[sheet_n]);
            #print("---")
        #print(list)
        if (os.path.exists('file_path.xls')):
            os.remove("file_path.xls")
        return list;
