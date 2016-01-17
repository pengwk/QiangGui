# _*_ coding:utf-8 _*_

import requests

import useragent


__doc__ = u"tyxk登录 返回cookie：PHPSESSID"

UserAgent = useragent.rand_agent()


def _header(Host=None, Cookie=None, Referer=None, ContentType=None, Origin=None):
    u"""产生header

    """
    general = {"Progma": "no-cache"}
    return nice_header


urls = {"login": "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=login",
        "check_login": "http://tyxk.dgut.edu.cn",
        "home": "http://tyxk.dgut.edu.cn/index.php?m=Home&c=Student&a=index",
        "cas_tyxk": "https://cas.dgut.edu.cn/?appid=tyxk",
        "cas_post": "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk",
        }
header = _header(Host="tyxk.dgut.edu.cn", )
cookies =
step_1 = requests.get(urls["login"], headers=)  # PHPSESSID

header =
cookies =
step_2 = requests.get(urls["check_login"], headers=, cookies=)

header =
cookies =
step_3 = requests.get(urls["cas_tyxk"], headers=, cookies=)

header =
cookies =
# __RequestVerificationToken
step_4 = requests.get(urls["cas_post"], headers=, cookies=)

header =
cookies =
step_5 = requests.post(urls["cas_post"], headers=, cookies=)  # .ASPAUTH

header =
cookies =
step_6 = requests.get(urls["cas_tyxk"], headers=, cookies=)

header =
cookies =
step_7 = requests.get(step_6.location, headers=, cookies=)  # platform=pc url

header =
cookies =
step_8 = requests.get(urls["home"], headers=, cookies=)

return PHPSESSID
