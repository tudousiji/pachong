import urllib.request
import sys
import http.cookiejar
import chardet
import urllib.response
import urllib.error
import requests
import hashlib

typeCode = sys.getfilesystemencoding()


class netUtils:
    @staticmethod
    def getData(parment):
        return netUtils.getRequests(parment);

    @staticmethod
    def getRequests(parment):
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

        isProxy = False;
        proxies = None
        if ('isProxy' in parment and parment['isProxy']):
            isProxy = True
            proxies = {parment['proxyProtocol']:  "http://" + parment['proxyIp'] + ":" + parment[
                'proxyPort']}

        isHeader = False;
        header=None;
        if ('isHeader' in parment):
            isHeader = True;
        if ('header' in parment):
            header = parment['header']


        isCookie = False;
        putCookie=None;
        if ('isCookie' in parment and parment['isCookie'] and parment['putCookie'] is not None):
            isCookie = True;
            putCookie=parment['putCookie'];


        # print(parment['url'])
        r=None
        isSuccess=True;
        url=parment['url'];
        try:
            if (requestType == 'GET'):
                r = requests.get(url=url, proxies=(proxies if isProxy else None),
                                 headers=netUtils.getHeaderDict(parment['url'],header), timeout=60,cookies=(putCookie if isCookie and putCookie  is not None else None))
            else:
                form = postData if requestType == 'POST' else None;
                #print(form)
                r = requests.post(url=url, data=form, proxies=(proxies if isProxy else None),
                                  headers=netUtils.getHeaderDict(parment['url'],header),
                                  timeout=60,cookies=(putCookie if isCookie and putCookie  is not None else None))
            #print(help(r.headers()))
        except Exception as err:
            isSuccess = False;
            #print(dir(err));
            print(err)



        if(r is not None):
            code = r.status_code;
            #print(code)
            print(r.text )
            if(code==200):
                if (r.encoding is not None ):
                    text = r.text;
                    body = text.encode(r.encoding).decode(r.apparent_encoding);
                    #print(text)
                else:
                    body = r.text

            else:
                isSuccess = False;
            r.close()
        else:
            isSuccess = False;

        if(isSuccess):
            content = {
                'body': body,
                'isProxy': isProxy,
                'postData': postData,
                'requestType': requestType,
                'url': url,
                'isHeader': isHeader,
                'header': r.headers,
                'isCookie': isCookie,
                'get_cookie': r.cookies,
                'put_cookie': 1,
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
                'put_cookie': 1,
                'isSuccess': isSuccess
            }

        if (r is not None):
            r.close();

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
        header=None;
        if ('isHeader' in parment):
            isHeader = True;
        if('header' in parment):
            header=parment['header']

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
            "Content-Type": "application/x-www-form-urlencoded",

        }
        if(b is not  None and type(b)==dict and len(b)>0):
            for x in b:
                headers[x]=str(b[x])
               # print(headers[x])
        return headers;



    @staticmethod
    def getTbkSign(cookie ,appKey,time,data):
        data=cookie + "&" + time + "&"+ appKey+"&"+data
        sign = hashlib.md5(data.encode('utf-8')).hexdigest();
        #print(sign)
        return sign


