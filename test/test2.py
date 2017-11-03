from selenium import webdriver
import time
import utils.netUtils
import config.config
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

def getUrl( cookie, page, accountId):
    if (cookie is None):
        cookie = "";
    times = str(int(round(time.time() * 1000)));
    data = urlPageListData.format(accountId,page)
    sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
    url = urlPageList.format(config.config.appkey, times, sign, data)
    return url;


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False
#driver=webdriver.PhantomJS(desired_capabilities=dcap);
driver=webdriver.PhantomJS();
driver.implicitly_wait(10)
driver.set_window_size(800, 600) # set browser size.
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)#这两种设置都进行才有效

url='https://market.m.taobao.com/apps/market/content/index.html?wh_weex=true&wx_navbar_transparent=true&contentId=200407221723&source=qingdan_dacu_itemlist&sourceType=other&suid=6093c86a-49bf-4430-bc80-8fb40594cd6f&ut_sk=1.WeR4Oo%2F7HAUDAJkS0LDdW3wU_21646297_1509531505748.TaoPassword-QQ.33&cpp=1&shareurl=true&spm=a313p.22.9q.75912251943&short_name=h.vdcPyG&app=chrome';
urlPageList='https://h5api.m.taobao.com/h5/mtop.taobao.daren.accountpage.feeds/1.0/?jsv=2.4.3&appKey={0}&t={1}&sign={2}&api=mtop.taobao.daren.accountpage.feeds&v=1.0&AntiCreep=true&type=jsonp&dataType=jsonp&data={3}'
urlPageListData='{{"accountId":{0},"force":2,"currentPage":{1}}}'

driver.get(url)
#print(driver.page_source)
#print('3: ', driver.get_cookies())
cookiesStr=driver.get_cookie("_m_h5_tk")['value'];
cookiesArr=cookiesStr.split("_");

for index in range(1,200):
    pageUrl = getUrl(cookiesArr[0], index, 723460593);
    print("pageUrl:", pageUrl)
    driver.get(pageUrl)
    #print(driver.page_source)
    #print(index,driver.page_source)
    text =driver.find_element_by_tag_name("body").text;
    body=json.loads(text)
    if(body['ret'][0]=='RGV587_ERROR::SM'):
        print("需要登录")
        driver.get("https://login.m.taobao.com/login.htm?from=sm&ttid=h5@iframe&tpl_redirect_url=https%3A%2F%2Fsec.taobao.com%2Fquery.htm%3Fstyle%3Dmiddle%26smApp%3Dmtop%26smPolicy%3Dmtop-daren_accountpage_feed-anti_Spider-checklogin%26smCharset%3DUTF-8%26smTag%3DMTE0LjI0OS4yNTUuOSwsOGIzZmU3YTUwOWU2NDhlMmE4NzkxN2I5MGZhMWU4M2U%253D%26smReturn%3Dhttps%253A%252F%252Fh5api.m.taobao.com%252Fh5%252Fmtop.taobao.daren.accountpage.feeds%252F1.0%252F%253Fhttps%253Don%2526jsv%253D2.4.3%2526appKey%253D12574478%2526t%253D1509615828831%2526sign%253D9638b83cf8e19cf981e056b02bdac35f%2526api%253Dmtop.taobao.daren.accountpage.feeds%2526v%253D1.0%2526AntiCreep%253Dtrue%2526type%253Djsonp%2526dataType%253Djsonp%2526data%253D%25257B%252522accountId%252522%253A723460593%252C%252522force%252522%253A2%252C%252522currentPage%252522%253A2%25257D%26smSign%3DrNe5ni9jIsdp9qZEcDvR%252FA%253D%253D")
        time.sleep(3)
        print(driver.page_source)
        driver.find_element_by_id("username").send_keys("123")
        driver.find_element_by_id("password").send_keys("321")
        driver.find_element_by_id("btn-submit").click();
        print(driver.page_source)
    else:
        print(body)
    #for item in driver.get_cookies():
    #    print(item["name"],":",item["value"])
    #print("-------------")
    time.sleep(3)




driver.quit()#退出浏览器


