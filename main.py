import socket;
import proxy.proxyUtils
import utils


dict = {
            'url': 'http://2017.ip138.com/ic.asp',
            'requestType': 'GET',
            'isProxy': True,
            'isHttps': False,
            'proxyProtocol':'http',
            'proxyIp':'60.23.39.219',
            'proxyPort':'80',
        }

ut = utils.netUtils.netUtils();
data = ut.getData(dict)
print(data)


#print(proxy.proxyUtils.proxyUtils.getLocalIp());


dict = {
            'url': 'http://www.xicidaili.com/nn/{0}',
            'requestType': 'GET',
            'isProxy': False,
            'isHttps': False,
            'index': 1,
            'reLoad':True,
        }
#data=proxy.proxyUtils.proxyUtils.getProxyList(dict);
