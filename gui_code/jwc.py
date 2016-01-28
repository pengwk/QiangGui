# _*_ coding: utf-8 _*_
import requests
import copy


def Headers(method,):
    base = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "Keep-Alive",
            "DNT": "1"}
    if  method == 'ajax':
        pass
    elif method == 'post':
        pass
    elif method == 'get':
        pass
    return headers


class JWC(object):

    """docstring for JWC"""

    def __init__(self, arg):
        super(JWC, self).__init__()
        self.urls = {
            'login': 'https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3djwxt&appid=jwxt',
            '': 'https://cas.dgut.edu.cn/?appid=jwxt'}
        self.baseheaders = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Encoding": "gzip, deflate, sdch",
                            "Accept-Language": "zh-CN,zh;q=0.8",
                            "Connection": "Keep-Alive",
                            "DNT": "1"}

    def Login(self, username, password):
        # get cookie BIG
        self._username = username
        self._password = password
        headers = copy.deepcopy(self.baseheaders)
        KeyHeaders = {"Host": "cas.dgut.edu.cn"
                      }
        headers.update(KeyHeaders)
        Cookie = requests.get(self.urls['login'],
                              headers=headers,
                              verify=False)

        BIG = Cookie['BIGipServerpl_cas_new']
        KeyHeaders = {"Host": "cas.dgut.edu.cn",
                      'Referer': self.urls['login'],
                      'Content-Type': 'application/x-www-form-urlencoded'
                      }
        data = {"Password": self._password,
                "ReturnUrl": r"/?appid=jwxt",
                "UserName": self._username
                }
        ASPX = requests.post(self.urls['login'],
                             headers=headers,
                             data=data,
                             verify=False)
