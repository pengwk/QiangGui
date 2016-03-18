# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import requests
import urlparse
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


def vertical_merge(img_top, img_bottom):
    u"""合并两个宽度相同的图像,垂直的方式
    img_top = StringIO(res.content)
    41pixel
    """
    top = Image.open(img_top)
    bottom = Image.open(img_bottom)
    width = top.width
    height = top.height + bottom.height - 41
    new_img = Image.new("RGB", (width, height))
    new_img.paste(top, (0, 0))
    crop = bottom.crop((0, 41, bottom.width, bottom.height))
    new_img.paste(crop, (0, top.height))
    return new_img

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
        # self.auth.headers.update(step_4.cookies)
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
        # get txt_xm
        step_1 = requests.get(urls["jwxt"] + "/jwweb/xscj/Stu_MyScore.aspx",
                              headers=_header(Host=urls["jwxt"][7:],
                                              Referer=urls["jwxt"] + "/jwweb/sys/menu.aspx"),
                              cookies=self.auth_cookie)
        save_html(step_1, "get_score_step_1.html")

        soup_1 = BeautifulSoup(step_1.text, 'lxml')
        txt_xm = soup_1.find_all(attrs={"name": "txt_xm"})[0]["value"]
        form_data = {"txt_xm": txt_xm,
                     "btn_search": "%BC%EC%CB%F7",
                     "SJ": "0",  # 0： 原始成绩 1：有效成绩
                     "SelXNXQ": "0",  # 0:入学以来 1：学年 2：学期
                     "zfx_flag": "0"  # 0：主修 1：辅修
                     }
        post = requests.post(urls["jwxt"] + "/jwweb/xscj/Stu_MyScore_rpt.aspx",
                             cookies=self.auth_cookie,
                             headers=_header(Host=urls["jwxt"][7:],
                                             Referer=urls["jwxt"] + "/jwweb/xscj/Stu_MyScore.aspx"),
                             data=form_data
                             )
        # 解析URL
        soup = BeautifulSoup(post.text, 'lxml')
        imgs = soup.find_all("img")
        # (xnxq, (filename, src, src))
        imgs_info = []
        for img in imgs:
            url = img["src"]
            # 20141:2014-2015学年第二学期 20140第一学期
            xnxq = urlparse.parse_qs(url.split("?")[1], True)["xnxq"][0]
            if xnxq in imgs_info:
                index = imgs_info.index(xnxq) + 1
                imgs_info[index].append(url)
            else:
                xn, xq = int(xnxq[:4]), int(xnxq[4:])
                filename = u"{}-{}学年第{}学期.png".format(xn, xn + 1, xq + 1)
                imgs_info.append(xnxq)
                imgs_info.append([filename, url])
        for index in xrange(1, len(imgs_info), 2):
            img_info = imgs_info[index]
            filename = img_info[0]
            if len(img_info) > 2:
                #
                def get_img(url):
                    res = requests.get(urls["jwxt"] + "/jwweb/xscj/" + url,
                                       headers=_header(Host=urls["jwxt"][7:],
                                                       Referer=urls["jwxt"] + "/jwweb/xscj/Stu_MyScore_rpt.aspx"),
                                       cookies=self.auth_cookie)
                    return res.content
                contents = [get_img(url) for url in img_info[1:]]
                imgfile = vertical_merge(
                    *[StringIO(content) for content in contents])
                imgfile.save(filename, format="png")
            else:
                url = img_info[1]
                res = requests.get(urls["jwxt"] + "/jwweb/xscj/" + url,
                                   headers=_header(Host=urls["jwxt"][7:],
                                                   Referer=urls["jwxt"] + "/jwweb/xscj/Stu_MyScore_rpt.aspx"),
                                   cookies=self.auth_cookie)
                imgfile = Image.open(StringIO(res.content))
                imgfile.save(filename, format="png")
        return None


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


class NICZY(object):
    u"""学校媒体资源网客户端
    http://niczy.dgut.edu.cn
    """

    def __init__(self, arg):
        super(NICZY, self).__init__()
        self.arg = arg

    def login(self):
        pass

    def logout(self):
        pass


class DgutCas(object):
    """docstring for ClassName"""

    def __init__(self, username, password):
        super(DgutCas, self).__init__()
        self._username = username
        self._password = password

    def cas(self, appid):
        u"""
        :param appid: string for example "tyxk" 
        :return: raise ValueError if given a wrong password else return location url
        """

        url = "https://cas.dgut.edu.cn"
        return_url = "/?appid={}".format(appid)
        
        params = {"ReturnUrl": return_url,
                  "appid": appid}

        data = {"UserName": self._username,
                "Password": self._password,
                "ReturnUrl": return_url,
                }

        session = requests.Session()
        session.headers["User-Agent"] = UserAgent
        session.verify = False

        get = session.get(url + "/User/Login", params=params,)

        token_name = "__RequestVerificationToken"
        token = self.get_form_token(get, token_name)
        data.update({token_name: token})
        
        session.headers["Referer"] = get.url

        post = session.post(get.url, data=data, allow_redirects=False)

        if post.status_code == 200:
            # 判断密码错误
            raise ValueError("wrong password error")
        elif post.status_code == 302:
            location = session.get(url + return_url, allow_redirects=False)
            return location.headers["location"]

    def get_form_token(self, response, token_name):
        u"""
        :param response: requests.Response object
        """

        soup = BeautifulSoup(response.text, "lxml")
        element = soup.find_all(attrs={"name": token_name})[0]
        return element["value"]

    def niczy(self, ):
        pass

    def tyxk(self, ):
        session = requests.Session()
        session.headers["User-Agent"] = UserAgent
        session.verify = False
        # 获取cookie php
        tyxk_home = "http://tyxk.dgut.edu.cn/index.php?m=&c=Index&a=login"
        while True:
            try:
                home = session.get(tyxk_home, timeout=6)
                if len(home.cookies) == 1:
                    break
            except requests.exceptions.Timeout:
                pass

        try:
            url = self.cas("tyxk")
        except ValueError:
            raise
        
        while True:
            try:
                get = session.get(url, timeout=6)
                if get.status_code == 500:
                    pass
                else:
                    return session
            except requests.exceptions.Timeout:
                pass

    def jwxt(self, ):
        pass

    def self_(self, ):
        pass

    def my(self, ):
        pass

    def yktcx(self, ):
        pass

    def wlbx(self, ):
        pass

def test():
    # import auth
    cas = auth.DgutCas("201441302623", "pwkilove5")
    tyxk = cas.cas("tyxk")

