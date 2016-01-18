# _*_ coding:utf-8 _*_

import requests

import useragent


__doc__ = u"tyxk登录 返回cookie：PHPSESSID"

requests.packages.urllib3.disable_warnings()

UserAgent = useragent.rand_agent()


def _header(ContentType=None, **_dict):
    u"""产生header
    第一个是位置参数ContentType因为连字符`-`不可用于关键字定义，其余是关键字参数
    """
    general = {"Progma": "no-cache",
               "User-Agent": UserAgent,
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Connection": "keep-alive",
               "Cache-Control": "no-cache"}
    if ContentType:
        general.update({"Content-Type": ContentType})
    general.update(_dict)
    return general


urls = {"login": "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=login",
        "check_login": "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=check_login",
        "home": "http://tyxk.dgut.edu.cn/index.php?m=Home&c=Student&a=index",
        "cas_tyxk": "https://cas.dgut.edu.cn/?appid=tyxk",
        "cas_post": "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk",
        "cas_host": "cas.dgut.edu.cn",
        "tyxk_host": "tyxk.dgut.edu.cn",
        "tyxk_base": "http://tyxk.dgut.edu.cn/",
        "cas_base": "https://cas.dgut.edu.cn"
        }

step_1 = requests.get(urls["login"],
                      headers=_header(Host=urls["tyxk_host"]),
                      allow_redirects=False,
                      verify=False)  # PHPSESSID


step_2 = requests.get(urls["check_login"],
                      headers=_header(Host=urls["tyxk_host"],
                                      Referer=step_1.url),
                      cookies=step_1.cookies,
                      allow_redirects=False,
                      verify=False)


step_3 = requests.get(urls["cas_tyxk"],
                      headers=_header(Host=urls["cas_host"],
                                      Referer=urls["tyxk_base"]),
                      # cookies=,
                      allow_redirects=False,
                      verify=False)


# __RequestVerificationToken
step_4 = requests.get(urls["cas_post"],
                      headers=_header(Host=urls["cas_host"],
                                      Referer=urls["tyxk_base"]),
                      # cookies=,
                      allow_redirects=False,
                      verify=False)

step_4_cookie = step_4.cookies.get_dict().items()[0]
form_data = {"UserName": "201441302623",
             "Password": "pwkilove5",
             "ReturnUrl": "/?appid=tyxk",
             step_4_cookie[0]: step_4_cookie[1] }

# .ASPAUTH
step_5 = requests.post(urls["cas_post"],
                       data=form_data,
                       headers=_header("application/x-www-form-urlencoded",
                                       Host=urls["cas_host"],
                                       Referer=urls["cas_post"],
                                       Origin=urls["cas_base"]
                                       ),
                       cookies=step_4.cookies,
                       allow_redirects=False,
                       verify=False)

step_6 = requests.get(urls["cas_tyxk"],
                      headers=_header(Host=urls["cas_host"],
                                      Referer=urls["cas_post"]),
                      cookies=(lambda a, b: b)(step_4.cookies.update(
                          step_5.cookies), step_4.cookies),
                      allow_redirects=False,
                      verify=False)


# platform=pc url
step_7 = requests.get(step_6.headers["location"],
                      headers=_header(Host=urls["tyxk_host"]),
                      cookies=step_1.cookies,
                      allow_redirects=False,
                      verify=False)


step_8 = requests.get(urls["home"],
                      headers=_header(Host=urls["tyxk_host"],
                                      Referer=step_7.url),
                      cookies=step_1.cookies,
                      allow_redirects=False,
                      verify=False)
print step_8.content
#return step_1.cookies, UserAgent
