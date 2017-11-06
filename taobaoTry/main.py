# 试用
import json
import taobaoTry.taobaoTryUtils
import utils.taobaokeUtils
import urllib.parse




#utils.taobaoTry.taobaoTry().handleDat(None,1,1)
taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, 0, 1)  # 第一个参数传入负数是精选，传0是所有的都采集
taobaoTry.taobaoTryUtils.taobaoTryUtils().handlePcTryList(None, -1, 1)  # 第一个参数传入负数是精选，传0是所有的都采集

#url="/report/view.htm?reportId=55616683&itemId=31682232";

