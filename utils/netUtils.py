import urllib.request
import sys
import http.cookiejar
import chardet
import urllib.response
import urllib.error
import requests
import hashlib
import config.config
from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver
import utils.logUtils
import traceback
from utils.logUtils import logUtils
typeCode = sys.getfilesystemencoding()
import gc


# from memory_profiler import profile
class netUtils:
    @staticmethod
    def getData(parment):
        if (type(parment) != dict):
            print("类型错误:" + type(parment));
            return;
        if ('url' not in parment):
            print("url 不存在");
            return;
        if('taskType' in parment and (parment['taskType']==config.config.taskType.BAIDU
                                      or parment['taskType']==config.config.taskType.COMMENT)):

            return netUtils.getRequestsForSelenium(parment);
        else:

            return netUtils.getRequests(parment);

    @staticmethod
    def getRequestsForSelenium(parment):
        logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium")
        global driver
        global isProxy
        global isSuccess
        global isCookie
        global putCookie
        global get_cookie
        global body
        global url

        isProxy = False;
        isSuccess = False;
        isCookie = False;
        putCookie = None;
        get_cookie = {}
        body = None
        url = None
        driver = None


        try:

            driver = webdriver.PhantomJS();
            # driver.implicitly_wait(3)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)  # 这两种设置都进行才有效
            proxy = webdriver.Proxy()
            if ('putCookie' in parment and parment['putCookie'] is not None):
                isCookie = True;
                putCookie = parment['putCookie'];
                driver.add_cookie(putCookie)

            if ('isProxy' in parment and parment['isProxy']):
                isProxy = True
                proxy.proxy_type = ProxyType.MANUAL
                proxy.http_proxy = parment['proxyIp'] + ':' + parment['proxyPort'];
                # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            else:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.DIRECT
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

            url = parment['url'];
            logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium 222")
            driver.get(url)
            logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium 333")
            # data = driver.page_source
            body = driver.find_element_by_tag_name("body").text
            if (driver.get_cookies() is not None):
                for item in driver.get_cookies():
                    # print(item["name"], ":", item["value"])
                    get_cookie[item["name"]] = item["value"]
        except Exception as err:
            logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium 444")
            errorData = traceback.format_exc()
            utils.logUtils.logUtils.info("error", str(errorData));
        finally:
            logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium 555")
            try:
                if (driver is not None):
                    driver.close()
                    driver.quit()
            except Exception as err:
                logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium driver.quit 777")
                errorData = traceback.format_exc()
                utils.logUtils.logUtils.info("error", str(errorData));

        if (body is not None and len(body) > 0):
            isSuccess = True
            content = {
                'body': body,
                'isProxy': isProxy,
                'postData': None,
                'requestType': 'GET',
                'url': url,
                'isHeader': False,
                'header': None,
                'code': None,
                'isCookie': isCookie,
                'get_cookie': get_cookie,
                'put_cookie': putCookie,
                'isSuccess': isSuccess
            }

        else:
            isSuccess = False
            content = {
                'body': None,
                'isProxy': isProxy,
                'postData': None,
                'requestType': 'GET',
                'url': url,
                'isHeader': False,
                'header': None,
                'code': None,
                'isCookie': isCookie,
                'get_cookie': get_cookie,
                'put_cookie': putCookie,
                'isSuccess': isSuccess
            }
        del driver
        del driver
        del isProxy
        del isSuccess
        del isCookie
        del putCookie
        del get_cookie
        del body
        del url
        gc.collect();
        logUtils.info("utils", "baiduKeyWordsPos getRequestsForSelenium 666")
        return content

    @staticmethod
    def getRequests(parment):
        requestType = 'GET';
        postData = "";
        if ('requestType' in parment):
            requestType = parment['requestType'].upper();
        if (requestType == 'GET'):
            # print("GET")
            pass
        else:
            if ('postData' in parment):
                postData = parment['postData']

        isProxy = False;
        proxies = None
        if ('isProxy' in parment and parment['isProxy']):
            isProxy = True
            proxies = {parment['proxyProtocol']: "http://" + parment['proxyIp'] + ":" + parment[
                'proxyPort']}

        isHeader = False;
        header = None;
        if ('isHeader' in parment):
            isHeader = True;
        if ('header' in parment):
            header = parment['header']

        isCookie = False;
        putCookie = None;
        if ('isCookie' in parment and parment['isCookie'] and parment['putCookie'] is not None):
            isCookie = True;
            putCookie = parment['putCookie'];
            # print(putCookie)

        # print(parment['url'])
        r = None
        isSuccess = True;
        url = parment['url'];
        errInfo = None;

        try:
            if (requestType == 'GET'):
                r = requests.get(url=url, proxies=(proxies if isProxy else None),
                                 headers=netUtils.getHeaderDict(parment['url'], header), timeout=60,
                                 cookies=(putCookie if isCookie and putCookie is not None else None), verify=False,
                                 allow_redirects=False)


            else:
                form = postData if requestType == 'POST' else None;
                # print(form)
                r = requests.post(url=url, data=form, proxies=(proxies if isProxy else None),
                                  headers=netUtils.getHeaderDict(parment['url'], header),
                                  timeout=60, cookies=(putCookie if isCookie and putCookie is not None else None))
                # print(help(r.headers()))
        except Exception as err:
            isSuccess = False;
            errInfo = err;
            print(err)

        if (r is not None):
            code = r.status_code;
            # print(code)
            # print(r.text,"---",url )
            if (code == 200):
                if (r.encoding is not None):
                    text = r.text;
                    if (len(text) > 0):
                        body = text.encode(r.encoding).decode(r.apparent_encoding, 'ignore');
                    else:
                        body = "";
                        # print(text)
                else:
                    body = r.text

            else:
                print("错误code:", code)
                print(r.text)
                isSuccess = False;
                # r.close()
        else:
            isSuccess = False;

        if (isSuccess):
            content = {
                'body': body,
                'isProxy': isProxy,
                'postData': postData,
                'requestType': requestType,
                'url': url,
                'isHeader': isHeader,
                'header': r.headers,
                'code': r.status_code,
                'isCookie': isCookie,
                'get_cookie': r.cookies,
                'put_cookie': putCookie,
                'isSuccess': isSuccess
            }
        else:
            content = {
                'err': errInfo,
                'isProxy': isProxy,
                'postData': postData,
                'requestType': requestType,
                'url': url,
                'code': r.status_code if r is not None else None,
                'get_cookie': r.cookies if r is not None else None,
                'isHeader': isHeader,
                'header': r.headers if r is not None else None,
                'isCookie': isCookie,
                'put_cookie': putCookie,
                'isSuccess': isSuccess
            }

        if (r is not None):
            r.close();

        del r;
        del body;
        del isProxy;
        del errInfo;
        del postData;
        del requestType;
        del url;
        del isHeader;
        del isCookie;
        del putCookie;
        del isSuccess;
        gc.collect();
        return content;

    @staticmethod
    def getUrllibData(parment):
        if (type(parment) != dict):
            print("类型错误:" + type(parment));
            return;
        if ('url' not in parment):
            print("url 不存在");
            return;
        requestType = 'GET';
        postData = "";
        if ('requestType' in parment):
            requestType = parment['requestType'].upper();
        if (requestType == 'GET'):
            # print("GET")
            pass
        else:
            if ('postData' in parment):
                postData = parment['postData']
                # print("POST")

        cookie = http.cookiejar.CookieJar()
        rq = urllib.request;
        rq.HTTPCookieProcessor(cookie);
        isProxy = False;
        proxy = None;
        if ('isProxy' in parment and parment['isProxy']):
            isProxy = parment['isProxy'];
            # print("isProxy:true")
            proxy = rq.ProxyHandler({parment['proxyProtocol']: parment['proxyIp'] + ":" + parment['proxyPort']});

        if (proxy == None):
            opener = rq.build_opener();
        else:
            opener = rq.build_opener(proxy);

        isCookie = False;
        if ('isCookie' in parment and parment['isCookie']):
            isCookie = True;
            rq.build_opener(rq.HTTPCookieProcessor(parment['isCookie']));

        isHeader = False;
        header = None;
        if ('isHeader' in parment):
            isHeader = True;
        if ('header' in parment):
            header = parment['header']

        url = parment['url'];

        opener.addheaders = netUtils.getHeaderList(url);
        form = postData if requestType == 'POST' else None;

        isSuccess = True;
        httpCode = -1;
        try:
            response = opener.open(url, form, 3000);
            data = response.read();
            httpCode = response.getcode();
            # print(httpCode==200)
            charset = chardet.detect(data)['encoding'];
            body = data.decode(charset, 'ignore');
            print(body)
            opener.close();
        except Exception as err:
            isSuccess = False;
            print(err)

        if (isSuccess and httpCode == 200):
            content = {
                'body': body,
                'isProxy': isProxy,
                'postData': postData,
                'requestType': requestType,
                'url': url,
                'isHeader': isHeader,
                'header': response.info(),
                'isCookie': isCookie,
                'cookie': cookie,
                'isSuccess': isSuccess
            }
        else:
            content = {
                'isProxy': isProxy,
                'postData': postData,
                'requestType': requestType,
                'url': url,
                'isHeader': isHeader,
                'isCookie': isCookie,
                'cookie': cookie,
                'isSuccess': isSuccess
            }
        return content;

    @staticmethod
    def getHeaderList(url):
        urlInfo = urllib.request.urlparse(url);
        headers = [
            ('Host', urlInfo.hostname),
            ('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'),
            ('Accept', ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', ' zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
            ('Accept-Encoding', 'deflate'),
            ('Referer', ' http://www.baidu.com'),
            ('Connection', ' keep-alive'),
            ('Cache-Control', ' max-age=0'),
        ]
        return headers;

    @staticmethod
    def getHeaderDict(url, b=None):

        urlInfo = urllib.request.urlparse(url);
        headers = {
            'Host': urlInfo.hostname,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        if (b is not None and type(b) == dict and len(b) > 0):
            for x in b:
                headers[x] = str(b[x])
                # print(headers[x])
        return headers;

    @staticmethod
    def getTbkSign(cookie, appKey, time, data):
        data = cookie + "&" + time + "&" + appKey + "&" + data
        sign = hashlib.md5(data.encode('utf-8')).hexdigest();
        # print(sign)
        return sign



        # from selenium import webdriver
        # driver=webdriver.PhantomJS();
        # driver.implicitly_wait(3)
        # driver.set_page_load_timeout(3)
        # driver.set_script_timeout(3)#这两种设置都进行才有效
        # for index in range(10000):
        #    url='http://zhannei.baidu.com/api/customsearch/keywords?title=小米手机怎么样/值得推荐吗'+(str)(index);
        # print("url:"+url)
        #    try:
        #        driver.get(url)
        # print(dir(driver))
        #        print((str)(index)+":"+ (str)(driver.page_source));
        #       print("-------------")
        #   except Exception as err:
        #       print(err)
        # driver.quit()#退出浏览器
