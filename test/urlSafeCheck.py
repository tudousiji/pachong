import utils.netUtils

class urlSafeCheck:
    def getData(self):
        url="https://cgi.urlsec.qq.com/index.php?m=check&a=check&callback=jQuery17209433636982690062_1510495181039&url=http://12277{0}.com&_=1510495181571"

        for index in range(0,10000):
            dict = {
                'url': url.format(index),
                'requestType': 'GET',
                'isProxy': False,
                'isHttps': True,
                'reLoad': True,
            }
            data = utils.netUtils.netUtils.getData(dict)
            print(index,":",data)
