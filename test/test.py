from selenium import webdriver
import time
import utils.netUtils
import config.config
from lxml import etree
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False
driver=webdriver.PhantomJS(desired_capabilities=dcap);
driver.implicitly_wait(10)
driver.set_window_size(800, 600) # set browser size.
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)#这两种设置都进行才有效
url='https://item.taobao.com/item.htm?id=559340609644';
for index in range(1,1000):
    driver.get(url)
    if("honor/荣耀 畅玩7X手机 全网通智能4G手机 荣耀7X"  in driver.page_source):
        data=driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a').click();
        # time.sleep(2)
        # data = driver.find_element_by_xpath('//*[@id="reviews"]')#.get_attribute('innerHTML')
        # if ("问大家" in data.text):
        #     data.find_element_by_xpath('//*[@id="reviews"]/div/ul/li[2]').click();
        #     time.sleep(2)
        #     data2=data.find_element_by_xpath('//*[@id="reviews"]/div/div/div/div/div[2]/div[2]').get_attribute('innerHTML');
        #     print(data2)
        # else:
        #     print("问大家，不存在")
    else:
        print("不存在")
    print(index,"-------------------------------------------------------------------------")

driver.quit()#退出浏览器


