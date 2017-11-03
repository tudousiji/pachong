from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False
driver=webdriver.PhantomJS(desired_capabilities=dcap);
driver.implicitly_wait(10)
driver.set_window_size(800, 600) # set browser size.
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)#这两种设置都进行才有效
url='https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=723460593&content_id=200407221723&spm=a21ye.index.account.d723460593';
for index in range(0,1000):
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="rx-block"]/div/div[3]/div/div[1]/div[1]').click();
    time.sleep(2)
    data = driver.find_element_by_xpath('//*[@id="rx-block"]/div').text
    print(data)
    print(index,"-----------------------")
