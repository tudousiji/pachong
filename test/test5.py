from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import utils.netUtils


def getData(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.loadImages"] = False
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Linux; Android 6.0.1; vivo Y66 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36 AliApp(TB/6.1.0.2) WindVane/8.0.0 720X1280 GCanvas/1.4.2.21"
    )
    driver = webdriver.PhantomJS(desired_capabilities=dcap);
    driver.implicitly_wait(10)
    driver.set_window_size(800, 600)  # set browser size.
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)  # 这两种设置都进行才有效
    # url='https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=723460593&content_id=200407221723&spm=a21ye.index.account.d723460593';
    for index in range(0, 1):
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="rx-block"]/div/div[3]/div/div[1]/div[1]').click();
        time.sleep(2)
        data = driver.find_element_by_xpath('//*[@id="rx-block"]/div').text
        print(data)
        print(index, "-----------------------")


dicts = {
    'url': "http://mytaobaoke/index.php/api/Daren/getDaRenList?page=1",
    'requestType': 'GET',
    'isProxy': False,
    'isHttps': True,
    'reLoad': True,
}

data = utils.netUtils.netUtils.getData(dicts)
body = json.loads(data['body'])['data']
for item in body:
    url = "https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=" + (str)(
        item['userId']) + "&content_id=" + (str)(item['userId']) + "&spm=a21ye.index.account.d723460593"
    print(url)
    getData(url)
