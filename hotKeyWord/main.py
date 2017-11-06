from collections import OrderedDict
import utils.utils
import hotKeyWord.keyWordUtils


def read_xls_file():
    dict = {
        'url': "http://index.1688.com/alizs/DownLoadExcel.do?cat=56&rankType=rise",
        'requestType': 'GET',
        'isProxy': False,
        'isHttps': False,
        'reLoad': True,
    }
    utils.utils.utils.parseXls(dict['url'])

data = hotKeyWord.keyWordUtils.keyWordUtils().getHotKeyWords()


