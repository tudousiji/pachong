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
getKeyWordsForSubKeyWordsNullList=serviceHost+'index.php/api/Keywords/getKeyWordsForSubKeyWordsNullList?page={0}&pageSize={1}';#获取关键词的衍生关键词为空的列表
addKeyWordsForSubKeyWordsNull=serviceHost+'index.php/api/Keywords/addKeyWordsForSubKeyWordsNull';#设置关键词的衍生关键词为空的
addGoodsItem=serviceHost+'index.php/api/AddGoods/addGoodsItem';#添加商品
getBuyinventoryCate = serviceHost + 'index.php/api/Buyinventory/getCateList';  # 获取淘宝必买清单分类
addbuyInventoryItemData = serviceHost + 'index.php/api/Buyinventory/addbuyInventoryItem';  # 添加必买清单
checkEffectiveContentIdList = serviceHost + 'index.php/api/Buyinventory/checkEffectiveContentIdList';  # 获取可以插入数据库的ContentId列表,暂时不用了
addContentId = serviceHost + 'index.php/api/Buyinventory/addContentId';  # 添加并且检查重复contentid
addBuyinventoryTags = serviceHost + 'index.php/api/Buyinventory/addBuyinventoryTags';  # 添加并且检查重复tags
getContentIdList = serviceHost + 'index.php/api/Buyinventory/getContentIdList';  # 获取未采集的ContentId

getProxyList='http://www.xicidaili.com/nn/{0}'
appkey='12574478';
pid="mm_29947721_14832832_57874820";
def enum(**enums):
    return type('Enum', (), enums)

taskType = enum(BAIDU=1, COMMENT=2)

keyWordsExtendList = ["淘宝优惠券", "天猫优惠券", "淘宝内部优惠券", "天猫内部优惠券", "京东优惠券"]
