# _*_ coding:utf-8 _*_
#!/usr/bin/env python

import requests
################
# 体育选课登陆 #
################

requests.packages.urllib3.disable_warnings()
class Physcial(object):

    def __init__(self, username, password):
        """准备"""
        self._username = username
        self._password = password
        self.userinfo = {'name': '',
                         'gender': '',
                         'campus': '',
                         'class': '',
                         'major': '',
                         'department': '',
                         'startyear': '',
                         'username': username,
                         'contact': ''}

        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch",
                        "Accept-Language": "zh-CN,zh;q=0.8",
                        "Connection": "Keep-Alive",
                        "Host": "tyxk.dgut.edu.cn",
                        "DNT": "1"}
        self.session.headers.update(self.headers)

        self.tyxk_base_url = "http://tyxk.dgut.edu.cn"
        self.cas_base_url = "https://cas.dgut.edu.cn"

        self.tyxk_login_url = self.tyxk_base_url + \
            "/index.php?m=&c=Index&a=login"
        self.tyxk_index_url = self.tyxk_base_url + \
            "/index.php?m=Home&c=Student&a=index"
        self.cas_login_url = self.cas_base_url + \
            "/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk"
        self.tyxk_check_login_url = self.tyxk_base_url + \
            "/index.php?m=&c=Index&a=check_login"
        self.cas_appid_url = self.cas_base_url + "/?appid=tyxk"

    def newlogin(self):
        """No auto """
        # 获取cookie PHPSESSID
        get_cookie_PHP = requests.get(self.tyxk_login_url,
                                      headers=self.prepare_headers("get", None))
        tyxk_cookie = get_cookie_PHP.cookies
        print "tyxk_cookie\n", tyxk_cookie
        #print get_cookie_PHP.text
        #   可能不需要
        v2 = requests.get(
            self.tyxk_check_login_url,
            cookies=tyxk_cookie,
            allow_redirects=False,
            headers=self.prepare_headers("get", self.tyxk_login_url)
        )
        print v2.text
        # 获取cookie BIGipServerpl_cas_new
        get_cookie_BIG = requests.get(
            self.cas_appid_url,
            headers=self.prepare_headers(
                "get", self.tyxk_base_url, "cas.dgut.edu.cn"),
            allow_redirects=False,
            verify=False)
        cas_cookies_BIG = get_cookie_BIG.cookies
        print "\ncas_cookies_BIG\n", cas_cookies_BIG
        print get_cookie_BIG.text
        cas_get = requests.get(self.cas_login_url,
                               headers=self.prepare_headers(
                                   "get", self.cas_appid_url, "cas.dgut.edu.cn"),
                               cookies=cas_cookies_BIG,
                               verify=False)
        #print "\ncas_get\n", cas_get.cookies
        #print cas_get.text
        # self.static = self.get_static(cas_get.cookies)
        # 可能需要先Get 登录并获取cookie .ASPXAUTH
        data = {"Password": self._password,
                "ReturnUrl": r"/?appid=tyxk",
                "UserName": self._username
                }

        cas_login = requests.post(
            self.cas_login_url,
            data=data,
            allow_redirects=False,
            headers=self.prepare_headers("post", self.cas_login_url),
            cookies=cas_cookies_BIG,
            verify=False)
        # 处理密码错误
        if cas_login.headers.get("Location") != "/?appid=tyxk":
            raise ValueError("usename or password error")

        cas_cookies_ASPX = cas_login.cookies
        #print "\ncas_cookies_ASPX\n", cas_cookies_ASPX
        #print cas_login.text
        # for token url
        if not len(cas_cookies_BIG.items()):
            cookie_BIG = cas_cookies_ASPX["BIGipServerpl_cas_new"]
            print "Not Default BIG"
        else:
            cookie_BIG = cas_cookies_BIG["BIGipServerpl_cas_new"]
            print "Default BIG"
        cas_cookies_BIG_ASPX = {".ASPXAUTH": cas_cookies_ASPX[".ASPXAUTH"],
                                "BIGipServerpl_cas_new": cookie_BIG}
        print "\ncas_cookies_BIG_ASPX\n", cas_cookies_BIG_ASPX
        get_token = requests.get(self.cas_appid_url,
                                 headers=self.prepare_headers("get",
                                                              self.cas_login_url,
                                                              "cas.dgut.edu.cn"),
                                 cookies=cas_cookies_BIG_ASPX,
                                 allow_redirects=False,
                                 verify=False
                                 )
        token_url = get_token.headers["Location"]
        #print "\ntoken url\n", token_url
        #print get_token.text
        verify_cookie = requests.get(token_url,
                                     cookies=tyxk_cookie,
                                     headers=self.prepare_headers("get", None,
                                                                  "tyxk.dgut.edu.cn"))
        #print "\nverify_cookie.headers\n", verify_cookie.headers
        #print verify_cookie.text
        self.session.cookies.set("PHPSESSID",
                                 tyxk_cookie["PHPSESSID"],
                                 domain='tyxk.dgut.edu.cn',
                                 path='/')
        tyxk_index = self.session.get(self.tyxk_index_url)
        self.get_user_info(tyxk_index)
        #print "\ntyxk_index\n", tyxk_index.cookies
        #print tyxk_index.text

        return (get_cookie_PHP, v2, get_cookie_BIG, cas_login, get_token, verify_cookie, tyxk_index)

    def get_static(self, cookies):
        req = []
        css_js_urls = ("https://cas.dgut.edu.cn/Content/cas.css",
                       "https://cas.dgut.edu.cn/Content/themes/custom-theme/jquery-ui-1.10.4.custom.css",
                       "https://cas.dgut.edu.cn/Scripts/jquery-1.8.2.min.js",
                       "https://cas.dgut.edu.cn/Scripts/jquery-ui-1.8.24.min.js",
                       "https://cas.dgut.edu.cn/Scripts/my.js")
        img_urls = ("https://cas.dgut.edu.cn/Content/m1.jpg",
                    "https://cas.dgut.edu.cn/Content/t1.jpg",
                    "https://cas.dgut.edu.cn/Content/dl.jpg",
                    "https://cas.dgut.edu.cn/Content/foot.jpg",
                    "https://cas.dgut.edu.cn/Content/btn.jpg")
        for url in css_js_urls:
            r = requests.get(url,
                             cookies=cookies,
                             headers=self.prepare_headers(
                                 "get", self.cas_login_url, "cas.dgut.edu.cn"),
                             verify=False)
            req.append(r)
        for url in img_urls:
            r = requests.get(url,
                             cookies=cookies,
                             headers=self.prepare_headers("get",
                                                          "https://cas.dgut.edu.cn/Content/cas.css",
                                                          "cas.dgut.edu.cn"),
                             verify=False)
            req.append(r)
        return req

    def get_user_info(self, page):
        mapdict = {'姓名': 'name',
                   '性别': 'gender',
                   '所在校区': 'campus',
                   '班级': 'class',
                   '专业': 'major',
                   '院系': 'department',
                   '学号': 'username',
                   '入学年份': 'startyear',
                   '联系方式': 'contact'}

        trs = bs4(page.content).find(id="studentInfo").find_all('tr')
        for tr in trs:
            data = tr.find_all("td")
            key = mapdict[data[0].get_text()]
            self.userinfo[key] = data[1].get_text().split()

    def login(self):
        """return a tuple of v1 v2 v3 v4"""
        v1 = self.session.get(self.tyxk_base_url)
        self.print_cookies()

        headers = {"Referer": v1.url,
                   "Cache-Control": "no-cache"}
        self.session.headers.update(headers)
        v2 = self.session.get(
            self.tyxk_base_url + "/index.php?m=&c=Index&a=check_login",
            verify=False)
        print v2.url
        self.print_cookies()
        headers = {"Referer": v2.url,
                   "Host": "cas.dgut.edu.cn",
                   "Origin": "https://cas.dgut.edu.cn",
                   "Content-Type": r"application/x-www-form-urlencoded"}
        self.session.headers.update(headers)

        data = {"Password": self._password,
                "ReturnUrl": r"/?appid=tyxk",
                "UserName": self._username
                }
        print "post to "
        v21 = self.session.get(
            "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk")
        v3 = self.session.post(
            "https://cas.dgut.edu.cn/User/Login?ReturnUrl=%2f%3fappid%3dtyxk&appid=tyxk", data=data, verify=False)
        self.print_cookies()
        # 清除登录表单格式
        self.session.headers.pop("Content-Type")
        self.session.headers.pop("Origin")
        # 模拟登陆成功跳转
        print "token pc", v3.url
        headers = {"Referer": v3.url}
        self.session.headers.update(headers)
        v4 = self.session.get(
            self.tyxk_base_url + "/index.php?m=Home&c=Student&a=index")

        # self.session.cookies.set(
        # "PHPSESSID", validCookie, domain='tyxk.dgut.edu.cn', path='/')
        self.print_cookies()
        # 准备异步加载
        headers = {"Referer": self.tyxk_base_url + "/index.php?m=Home&c=Student&a=index",
                   "Host": "tyxk.dgut.edu.cn",
                   # 加入异步加载header
                   "Accept": r"*/*",
                   "Pragma": "no-cache",
                   "X-Requested-With": "XMLHttpRequest"
                   }
        self.session.headers.update(headers)

        # 不确定

        # self.session.cookies.clear(
        # domain="tyxk.dgut.edu.cn", path='/', name="BIGipServerpl_cas_new")

        if v3.ok:
            print "login successed"
        else:
            print "login failed"

        return (v1, v2, v3, v4)

    def prepare_headers(self, type, referer, host=None):
        """:type post get ajax"""
        import copy
        headers = copy.deepcopy(self.headers)
        if type == 'ajax':
            ajax_headers = {"Referer": self.tyxk_index_url,
                            "Host": "tyxk.dgut.edu.cn",
                            "Accept": r"*/*",
                            "Pragma": "no-cache",
                            "X-Requested-With": "XMLHttpRequest"
                            }
            headers.update(ajax_headers)
        elif type == 'post':
            post_headers = {"Referer": self.cas_login_url,
                            "Host": "cas.dgut.edu.cn",
                            "Cache-Control": "no-cache",
                            "Pragma": "no-cache",
                            "Origin": "https://cas.dgut.edu.cn",
                            "Content-Length": 48 + len(self._username) + len(self._password),
                            "Content-Type": r"application/x-www-form-urlencoded"}
            headers.update(post_headers)
            print headers
        elif type == 'get':
            if referer != None:
                get_headers = {"Referer": referer,
                               "Host": host}
                headers.update(get_headers)
            print "get ", headers
        return headers

    def logout(self):
        # 清除异步header
        v1 = self.session.get(
            self.tyxk_base_url + "/index.php?m=&c=Index&a=user_exit")
        if v1.ok:
            print 1
        else:
            print 0
        return v1

    def getCourseList(self, page):
        """All Course List"""
        params = {"p": page}
        v1 = self.session.get(
            self.tyxk_base_url + "/index.php?m=&c=Student&a=courseList",
            params=params,
            headers=self.prepare_headers("ajax", None))
        # 打印返回内容 可以显示中文
        print v1.text
        return v1

    def getAbleCourse(self, page):
        """可选课程"""
        params = {"p": page}
        v1 = self.session.get(
            self.tyxk_base_url + "/index.php?m=&c=Student&a=ableCourseList",
            params=params,
            headers=self.prepare_headers("ajax", None))
        print v1.text
        return v1

    def getSelectedList(self):
        v1 = self.session.get(
            self.tyxk_base_url +
            "/index.php?m=&c=Student&a=selectedCourseList",
            headers=self.prepare_headers("ajax", None))
        print v1.text
        return v1

    def selectCourse(self, courseId, method):
        """@method: quit" or select """
        data = {"course_id": courseId,
                "method": method}
        v1 = self.session.post(
            self.tyxk_base_url + "/index.php?m=&c=Student&a=courseSelect",
            data=data,
            headers=self.prepare_headers("ajax", None))
        print v1.text
        return v1

    def getResult(self):
        '''课表结果'''
        print self.session.headers
        print self.session.cookies
        v1 = self.session.get(
            self.tyxk_base_url +
            "/index.php?m=&c=Student&a=selectCourseResult",
            headers=self.prepare_headers("ajax", None))
        print v1.text
        return v1

    def print_cookies(self):
        cookies = self.session.cookies.iteritems()
        for cookie in cookies:
            print cookie
    # def
############################
# data = "\u53f2\u5b89\u7fce"
# print data.decode("unicode_escape")
# 可以显示中文
# data有反斜杠时使用data.decode('raw_unicode_escape')
# os.chdir("C:\Users\wk\Desktop\code\myproject")
# https://www.python.org/ftp/python/2.7.8/python-2.7.8-pdb.zip
# import login
# reload(login)
# me = login.Physcial("201441302623",'pwkilove5')
# lr = me.login()
# me.getResult()

# requests 的cookies 修改查看 clear
# 查看请求的cookies
# 登录错误

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    me = Physcial("201441302623", 'pwkilove5')
    lr = me.newlogin()
    me.getResult()


def main():
    requests.packages.urllib3.disable_warnings()
    me = Physcial("201441302625", 'tongxin123')
    # me = Physcial("201441302623", 'pwkilove5')
    try:
        lr = me.newlogin()
        result = me.getResult()
        me.logout()
    except ValueError:
        print u'请重新输入密码'
    except ConnectTimeout:
        pass
    except Timeout:
        pass
    except ReadTimeout:
        pass
    except ConnectionError:
        pass
    except HTTPError:
        pass
    # lr = me.newlogin()
    # result = me.getResult()
    # me.logout()
# 先手工后找原因 太年轻
 # from bs4 import BeautifulSoup as bs4
 # trs = bs4(s).find(id="studentInfo").tr
 # for tr in trs:
 #    data = tr.td
 #    print data[0].get_text()
 #    print data[1].get_text()
