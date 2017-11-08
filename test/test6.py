from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import utils.netUtils

options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 6.0.1; vivo Y66 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36 AliApp(TB/6.1.0.2) WindVane/8.0.0 720X1280 GCanvas/1.4.2.21"')
browser = webdriver.Chrome(chrome_options=options)
url = "https://daren.taobao.com/account_page/daren_home.htm?wh_weex=true&user_id=667241583&content_id=667241583&spm=a21ye.index.account.d723460593"
browser.get(url)
# browser.quit()
