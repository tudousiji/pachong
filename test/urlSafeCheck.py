import utils.netUtils

class urlSafeCheck:
    def getData(self):
        url="https://cgi.urlsec.qq.com/index.php?m=check&a=check&callback=jQuery17209433636982690062_1510495181039&url=http://122779.com&_=1510495181571"
        dict = {
            'url': url,
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': True,
            'reLoad': True,
        }
        for index in range(0,1000):
            data = utils.netUtils.netUtils.getData(dict)
            print(index,":",data)
