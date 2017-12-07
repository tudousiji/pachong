buyInventoryListUrl = "https://acs.m.taobao.com/h5/mtop.taobao.tceget.steins.qingdan.xget/1.0/?appKey={0}&t={1}&sign={2}&AntiCreep=true&api=mtop.taobao.tceget.steins.qingdan.xget&v=1.0&dataType=jsonp&timeout=20000&type=jsonp&callback=mtopjsonp1&data={3}"
buyInventoryListData = '{"d":"{\\"tce_sid\\":\\"1891397\\",\\"tce_vid\\":\\"0\\",\\"tid\\":\\"\\",\\"tab\\":\\"%s\\",\\"topic\\":\\"%s\\",\\"count\\":\\"\\",\\"pageSize\\":\\"%s\\",\\"pageNo\\":\\"1\\",\\"env\\":\\"online\\",\\"psId\\":\\"%s\\",\\"currentPage\\":\\"%s\\",\\"sceneId\\":\\"%s\\",\\"src\\":\\"phone\\"}"}';
# listPageSize = 500

buyInventoryItemUrl = 'http://acs.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/?appKey={0}&t={1}&sign={2}&api=mtop.taobao.beehive.detail.contentservicenew&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={3}'
buyInventoryItemData = '{{"contentId":"{0}","source":"qingdan_gonglie","type":"h5","params":"{{\\"business_spm\\":\\"a3145.8183741\\"}}"}}';

buyInventoryTags = "https://market.m.taobao.com/apps/market/qingdan/label-11.html?wh_weex=true&tag=这些情侣杯秀恩爱必备&sourceFlag=1&wx_navbar_transparent=true";
