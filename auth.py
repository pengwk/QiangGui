# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
import requests
import logging
import time
import useragent

__doc__ = u"tyxk登录 返回cookie：PHPSESSID"

logging.basicConfig(
    format="%(levelname)-10s %(message)s",
    level=logging.DEBUG)

log = logging.getLogger("auth")
handler = logging.FileHandler("auth.log")
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


requests.packages.urllib3.disable_warnings()

UserAgent = useragent.rand_agent()
STREAM_FLAG = False


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


def hidden_form(postpage):
    u"""postpage 必须是resopse.text
    """
    _dict = {}
    soup = BeautifulSoup(postpage, "lxml")
    hiddens = soup.form.find_all(attrs={"type": "hidden"})
    for hidden in hiddens:
        _dict[hidden["name"]] = hidden["value"]
    return _dict


def save_html(response, filename):
    u"""保存requests库请求的页面
    用于调试
    """
    with open(filename, "wb") as html:
        html.write(response.content)
    return None

urls = {"login": "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=login",
        "check_login": "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=check_login",
        "home": "http://tyxk.dgut.edu.cn/index.php?m=Home&c=Student&a=index",
        "cas_tyxk": "https://cas.dgut.edu.cn/?appid=tyxk",
        "cas_post": "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk",
        "cas_host": "cas.dgut.edu.cn",
        "tyxk_host": "tyxk.dgut.edu.cn",
        "tyxk_base": "http://tyxk.dgut.edu.cn/",
        "cas_base": "https://cas.dgut.edu.cn",
        #"jwxt": "http://jwxt.dgut.edu.cn/jwweb/",
        "cas_jwxt": "https://cas.dgut.edu.cn/?appid=jwxt",
        "jwxt_post": "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3djwxt&appid=jwxt",
        "jwxt_host": "jwxt.dgut.edu.cn",
        "jwxt_logout": "http://jwxt.dgut.edu.cn/jwweb/sys/Logout.aspx",

        # new url system
        "cas": "https://cas.dgut.edu.cn",
        "jwxt": "http://jwxt.dgut.edu.cn",
        "tyxk": "http://tyxk.dgut.edu.cn"
        }


# return step_1.cookies, UserAgent


class JWCAuth(object):
    """docstring for jwcAuth"""

    def __init__(self, username, password):
        super(JWCAuth, self).__init__()
        self.post_dict = {"UserName": username,
                          "Password": password}
        self.auth_cookie = None
        self.auth = requests.Session()
        self.auth.headers.update(_header())

    def login(self):

        step_1 = requests.get(urls["cas"] + "/User/Login",  # urls["jwxt_post"],
                              params={"ReturnUrl": "/?appid=jwxt",
                                      "appid": "jwxt"},
                              headers=_header(Host=urls["cas_host"]),
                              allow_redirects=False,
                              verify=False,
                              stream=STREAM_FLAG)
        # for debug
        save_html(step_1, "step_1.html")
        log.debug("\nstep_1\nRequest:\n{}\nResponse:\n{}".format(
            step_1.url, step_1.headers))
        time.sleep(2)

        hiddens = hidden_form(step_1.text)
        form_data = (lambda a, b: b)(hiddens.update(self.post_dict), hiddens)
        step_2 = requests.post(step_1.url,  # urls["jwxt_post"],
                               headers=_header("application/x-www-form-urlencoded",
                                               Host=urls["cas"][8:],
                                               Referer=step_1.url),
                               cookies=step_1.cookies,
                               data=form_data,
                               allow_redirects=False,
                               verify=False,
                               stream=STREAM_FLAG
                               )
        save_html(step_2, "step_2.html")
        log.debug("\nstep_2\nRequest:\n{}\nResponse:\n{}".format(
            step_2.url, step_2.headers))
        time.sleep(0.5)

        step_3 = requests.get(urls["cas"],
                              params={"appid": "jwxt"},
                              headers=_header(Host=urls["cas"][8:],
                                              Referer=step_1.url),
                              allow_redirects=False,
                              verify=False,
                              cookies=(lambda a, b: b)(step_1.cookies.update(
                                  step_2.cookies), step_1.cookies),
                              stream=STREAM_FLAG
                              )
        log.debug("\nstep_3\nRequest:\n{}\nResponse:\n{}".format(
            step_3.url, step_3.headers))
        save_html(step_3, "step_3.html")
        time.sleep(0.5)
        step_4 = requests.get(step_3.headers["location"],
                              headers=_header(Host=urls["jwxt"][7:]),
                              allow_redirects=False,
                              verify=False,
                              stream=STREAM_FLAG)
        log.debug("\nstep_4\nRequest:\n{}\nResponse:\n{}".format(
            step_4.url, step_4.headers))
        save_html(step_4, "step_4.html")
        self.auth_cookie = step_4.cookies
        self.auth.headers.update(step_4.cookies)
        return None

    def never_give_up(self):
        try_num = 0
        while True:
            try:
                try_num += 1
                return self.login()
            except:
                pass

    def logout(self):
        res = requests.get(urls["jwxt"] + "/jwweb/sys/Logout.aspx",
                           cookies=self.auth_cookie,
                           headers=_header(Host=urls["jwxt_host"],
                                           Referer=urls["jwxt"] + "/jwweb/SYS/Main_tools.aspx"),
                           allow_redirects=False,
                           verify=False)
        return res

    def get_score(self):
        form_data = {}
        post = requests.get(urls["jwxt"] + "/jwweb/xscj/Stu_MyScore_rpt.aspx",
                            cookies=self.auth_cookie,
                            headers=_header("application/x-www-form-urlencoded",
                                            Host=urls[jwxt][7:],
                                            Referer=urls["jwxt"] + "/jwweb/xscj/Stu_MyScore.aspx",),
                            )


class TYXKAuth(object):
    """docstring for TyxkAuth"""

    def __init__(self, arg):
        super(TYXKAuth, self).__init__()
        self.arg = arg

    def login(self, username, password):
        u"""
        """
        try:
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

            # step_4_cookie = step_4.cookies.get_dict().items()[0]
            # 表单里的是用来检测是否交换的

            form_data = {"UserName": "201441302623",
                         "Password": "pwkilove5",
                         "ReturnUrl": "/?appid=tyxk",
                         step_4_cookie[0]: step_4_cookie[1]}

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
            return step_1.cookies
        except:
            return None

    def logout(self):
        pass
