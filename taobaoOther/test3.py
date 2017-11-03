from selenium import webdriver
import time
import utils.netUtils
import config.config







def getUrl( cookie, page, accountId):
    if (cookie is None):
        cookie = "";
    times = str(int(round(time.time() * 1000)));
    data = urlPageListData.format(accountId,page)
    sign = utils.netUtils.netUtils.getTbkSign(cookie, config.config.appkey, times, data)
    url = urlPageList.format(config.config.appkey, times, sign, data)
    return url;


driver=webdriver.PhantomJS();
driver.implicitly_wait(10)
driver.set_window_size(800, 600) # set browser size.
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)#这两种设置都进行才有效

url='https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=723460593&spm=a21ye.index.account.d723460593';
urlPageList='https://h5api.m.taobao.com/h5/mtop.taobao.daren.accountpage.feeds/1.0/?jsv=2.4.3&appKey={0}&t={1}&sign={2}&api=mtop.taobao.daren.accountpage.feeds&v=1.0&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp3&data={3}'
urlPageListData='{{"accountId":{0},"force":2,"currentPage":{1}}}'

driver.get(url)
#print(driver.page_source)
#print('3: ', driver.get_cookies())
cookiesStr=driver.get_cookie("_m_h5_tk")['value'];
cookiesArr=cookiesStr.split("_");

for index in range(1,2):
    pageUrl = getUrl(cookiesArr[0], index, 723460593);
    print("pageUrl:", pageUrl)
    driver.get(pageUrl)
    #print(driver.page_source)
    print(index,driver.page_source)
    body =driver.find_element_by_tag_name("body");
    print(body.text)
    for item in driver.get_cookies():
        print(item["name"],":",item["value"])
    print("-------------")
    time.sleep(3)




driver.quit()#退出浏览器


