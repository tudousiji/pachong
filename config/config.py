serviceHost='http://mytaobaoke/'
checkProxyStatusUrl='http://2017.ip138.com/ic.asp'
addProxyIpUrl=serviceHost+'index.php/api/Proxyip/addProxyIp';#添加代理ip
updateFailProxyIp=serviceHost+'index.php/api/Proxyip/updateFailProxyIp';#更新失败代理ip
getNextProxyIpList=serviceHost+'index.php/api/Proxyip/getNextProxyIpList?page={0}'
addDarenUrl=serviceHost+'index.php/api/Daren/addDaRenUrlForList';#添加达人列表
getDaRenHomeUrl=serviceHost+'index.php/api/Daren/getDaRenUrl';#获取达人首页地址
addTaobaoTryUrl=serviceHost+'index.php/api/Tryout/addTaobaoTry';#增加试用数据
checkEffectiveTaobaoTryIdListUrl=serviceHost+'index.php/api/Tryout/checkEffectiveTaobaoTryIdListUrl';#检测试用数据
addHotKeyWords=serviceHost+'index.php/api/Keywords/addHotKeyWords'#添加热门关键词，采集来源来自阿离爸爸
getTryCate=serviceHost+'index.php/api/Tryout/getCateId'#获取淘宝试用id
getTaoBaoItemInfoList=serviceHost+'index.php/api/Taobaoinfo/getTaobaoInfoList'#采集百度分词，评论，问大家等
addTaoBaoItemInfo=serviceHost+'index.php/api/Taobaoinfo/addTaobaoItemInfo'#采集百度分词，评论，问大家等
getKeyWordsList=serviceHost+'index.php/api/Keywords/getKeyWordsList?page={0}&pageSize={1}';#获取关键词列表
addGoodsItem=serviceHost+'index.php/api/AddGoods/addGoodsItem';#添加商品
getProxyList='http://www.xicidaili.com/nn/{0}'
appkey='12574478';
pid="mm_29947721_14832832_57874820";
def enum(**enums):
    return type('Enum', (), enums)

taskType = enum(BAIDU=1, COMMENT=2)