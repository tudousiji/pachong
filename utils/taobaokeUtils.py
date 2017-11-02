


import random
import requests


class taobaokeUtils:
    taobaoToKen=[]






    #获取淘宝客cookies
    @staticmethod
    def getCookies():
        if (len(taobaokeUtils.taobaoToKen) > 0):
            index = random.randint(0, len(taobaokeUtils.taobaoToKen) - 1)
            cookiesDict = taobaokeUtils.taobaoToKen[index];
            cookieArr = cookiesDict['_m_h5_tk'].split('_')
            dict = {
                'cookies':cookieArr[0],
                'putCookie':cookiesDict,
                'index':index,
            }
            return dict;
        else:
            cookie = {'_m_h5_tk': "",
                      '_m_h5_tk_enc': ""}
            dict = {
                'cookies': None,
                'putCookie': None
            }
            return dict

    #设置cookies
    @staticmethod
    def putCookies(cookies):
        cookie = {'_m_h5_tk': cookies['_m_h5_tk'],
                  '_m_h5_tk_enc': cookies['_m_h5_tk_enc'],
                  }
        #dictCookies = requests.utils.dict_from_cookiejar(cookies);
        #print(dictCookies.get('cna'))
        if(('cna') in cookies):
            cookie['cna']=cookies['cna'];

        taobaokeUtils.taobaoToKen.append(cookie)
        return cookie

    @staticmethod
    def reMoveCookies(index):
        del taobaokeUtils.taobaoToKen[index]




