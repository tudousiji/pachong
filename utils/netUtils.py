import urllib.request
import sys
import http.cookiejar
import chardet
import urllib.response
import urllib.error


typeCode = sys.getfilesystemencoding()
class netUtils:
    @staticmethod
    def getData(parment):
        if( type(parment) != dict):
            print("类型错误:"+type(parment) );
            return ;
        if ('url' not in parment):
            print("url 不存在");
            return ;
        requestType='GET';
        postData="";
        if('requestType' in parment):
            requestType=parment['requestType'].upper();
        if(requestType == 'GET'):
            #print("GET")
            pass
        else:
            if ('postData' in parment):
                postData=parment['postData']
                #print("POST")

        cookie = http.cookiejar.CookieJar()
        rq = urllib.request;
        rq.HTTPCookieProcessor(cookie);
        isProxy=False;
        proxy=None;
        if ('isProxy' in parment and parment['isProxy']):
            isProxy=parment['isProxy'];
            proxy = rq.ProxyHandler({parment['proxyProtocol']:parment['proxyIp']+":"+parment['proxyPort']});

        if(proxy == None):
            opener = rq.build_opener();
        else:
            opener = rq.build_opener(proxy);

        isCookie=False;
        if ('isCookie' in parment and parment['isCookie']):
            isCookie=True;
            rq.build_opener(rq.HTTPCookieProcessor(parment['isCookie']));

        isHeader=False;
        if('isHeader' in parment):
            isHeader=True;

        url=parment['url'];
        opener.addheaders=netUtils.getHeader(url);
        form = postData if requestType=='POST' else None;

        isSuccess=True;
        httpCode=-1;
        try:
            response = opener.open(url, form, 10000);
            data = response.read();
            httpCode=response.getcode();
            #print(httpCode==200)
            charset = chardet.detect(data)['encoding'];
            body = data.decode(charset, 'ignore');
            opener.close();
        except Exception as err:
            isSuccess=False;
            #print(err)



        if(isSuccess and httpCode==200):
            content={
                'body':body,
                'isProxy':isProxy,
                'postData':postData,
                'requestType':requestType,
                'url':url,
                'isHeader':isHeader,
                'header':response.info(),
                'isCookie':isCookie,
                'cookie':cookie,
                'isSuccess':isSuccess
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
    def getHeader(url):
        urlInfo= urllib.request.urlparse(url);
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