from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get('https://login.m.taobao.com/login.htm?_input_charset=utf-8&ttid=h5%40iframe')
time.sleep(1)
browser.find_element_by_id("username").send_keys("duanzheng2");
browser.find_element_by_id("password").send_keys("duanzheng2");
#browser.find_element_by_id("btn-submit").click()
#browser.find_element_by_id().


