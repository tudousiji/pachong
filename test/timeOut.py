from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver

driver = None
try:
    driver = webdriver.PhantomJS();
    # driver.implicitly_wait(3)
    driver.set_page_load_timeout(3)
    driver.set_script_timeout(3)  # 这两种设置都进行才有效
    proxy = webdriver.Proxy()
    driver.get("http://zhannei.baidu.com/api/customsearch/keywords?title=小米手机怎么样???");
    data = driver.page_source;
except Exception as err:
    print("error")
finally:
    print("finally")
    if (driver is not None):
        driver.close()
        driver.quit()
