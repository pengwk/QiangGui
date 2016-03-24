# _*_ coding:utf-8 _*_

import json
import os
import time

import requests
from bs4 import BeautifulSoup

import auth


class PhysicalClient(object):
    u""""""

    def __init__(self, session):
        self.url = "http://tyxk.dgut.edu.cn/index.php"
        self.s = session
        self.ajax = session
        self.ajax.headers["X-Requested-With"] = "XMLHttpRequest"
        self.dirty_course_list = []
        self.clean_course_list = []
        self.dirty_able_list = []
        self.clean_able_list = []
        self.selected_list = []
        self.user_info = {}
        self.announcement = None
        self.score_list = []
        self.course_result = None

    def get_all_course(self):
        u"""下载全校课程数据，保存成一个列表"""

        page_start = 1
        page_one = self._get_single_page("1")
        if page_one is None:
            return None
        else:
            self.dirty_course_list.append(page_one)
            page_end = self._get_page_end(page_one["page"])
        for index in xrange(2, page_end + 1):
            page = self._get_single_page(index)
            self.dirty_course_list.append(page)
        return None

    def get_able_course(self, page_index):
        params = {"m": "",
                  "c": "Student",
                  "a": "ableCourseList",
                  "p": page_index}
        res = self.ajax.get(self.url, params=params)
        res_json = res.json()
        if res_json["mes"] == False:
            # 非选课时间或者处于免修状态
            return False
        elif res_json["course"] == None:
            # 检索内容为空
            return None
        elif res:
            # 页数
            # 下载
            return None

    def get_selected(self):
        params = {"c": "Student",
                  "m": "",
                  "a": "selectedCourseList"}
        res = self.ajax.get(self.url, params=params,)
        res_json = res.json()
        if res_json["mes"] == False:
            return False
        elif res_json["course"] == None:
            return None
        else:
            pass

    def get_result(self):
        u"""包含老师信息"""
        params = {"c": "Student",
                  "m": "",
                  "a": "selectCourseResult"}
        res = self.ajax.get(self.url, params=params)
        res_json = res.json()
        if res_json == []:
            # No Related Information
            return None
        else:
            self.course_result = res_json
            return res_json

    def select(self, course_id):
        params = {"m": "",
                  "c": "Student",
                  "a": "courseSelect"}
        data = {"method": "sel",
                "course_id": course_id}
        while True:
            try:
                res = self.ajax.post(self.url, params=params,
                                     data=data, timeout=2,)
                print res.text
                if res.status_code == 500:
                    pass
                else:
                    return None
            except requests.exceptions.Timeout:
                pass

    def unselect(self, course_id):
        params = {"m": "",
                  "c": "Student",
                  "a": "courseSelect"}
        data = {"method": "quit",
                "course_id": course_id}
        res = self.ajax.post(url, params=params, data=data,)
        print res.text
        return None

    def get_user_info(self):
        params = {"m": "Home",
                  "c": "Student",
                  "a": "index"}
        res = self.s.get(self.url, params=params)
        soup = BeautifulSoup(res.text)
        # 个人信息
        student_info = soup.find_all(attrs={"id": "studentInfo"})[0]
        trs = student_info.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            key = tds[0].string.strip()
            value = tds[1].string.strip()
            self.user_info[key] = value
        # 体测 期末 成绩
        score = soup.find_all(attrs={"id": "checkScore"})[0]
        trs = score.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            _dict = {}
            _dict[u"school_year"] = tds[0].string.strip()
            _dict[u"school_term"] = tds[1].string.strip()
            _dict[u"fitness"] = tds[2].string.strip()
            _dict[u"fitness_judge"] = tds[3].string.strip()
            _dict[u"final_score"] = tds[4].string.strip()
            self.score_list.append(_dict)
        # 管理员公告
        div = soup.find_all(attrs={"id": "studentAd"})[0]
        self.announcement = div.div.div.string.strip()
        return None

    def get_score(self):
        pass

    @property
    def get_announcement(self):

        return self.announcement

    def logout(self):
        params = {"m": "",
                  "c": "Index",
                  "a": "user_exit"}
        res = self.s.get(self.url, params=params)
        if res.status_code == 200:
            return None

    def _get_single_page(self, page_index):
        u"""
        :return: 没有课程发布时返回None
        """
        params = {"m": "",
                  "c": "Student",
                  "a": "courseList",
                  "p": page_index}
        while True:
            try:
                res = self.ajax.get(self.url, params=params,
                                    timeout=4)
                res_json = res.json()
                if res_json["allCourse"] is None:
                    return None
                else:
                    return res_json
            except requests.exceptions.Timeout:
                pass

    def _get_page_end(self, text):
        soup = BeautifulSoup(text, "lxml")
        str_ = soup.find_all("a")[-1].string
        return int(str_)

    def save_course(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f)
        return None

    def classify_course(self):

        dicts_list = [{}, {}, {}, {}, {}]
        keys = ["name", "course_name", "campus", "day", "time"]

        for course in self.clean_course_list:
            for index, key in enumerate(keys):
                value = course[key]
                if value in dicts_list[index]:
                    dicts_list[index][value].append(course)
                else:
                    dicts_list[index][value] = [course]

        dicts = {}
        for x in xrange(0, 5):
            dicts[keys[x]] = dicts_list[x]

        self.classify_course_dict = dicts
        return None

    def gen_clean_course(self):
        for index, dirty in enumerate(self.dirty_course_list):
            course_list = dirty["allCourse"]
            for course in course_list:
                course["page"] = index
                self.clean_course_list.append(course)


def s(username, password, course_id_list):
    cas = auth.DgutCas(username, password)
    session = cas.tyxk()
    client = PhysicalClient(session)
    for id in course_id_list:
        client.select(id)


class Niczy(object):
    u""""""

    def __init__(self, session):
        super(Niczy, self).__init__()
        self.s = session
        self.ajax = session
        self.ajax.headers["X-Requested-With"] = "XMLHttpRequest"
        self.home = "http://niczy.dgut.edu.cn"

    def logout(self,):
        url = self.home + "/sso/logout.php"
        res = self.s.get(url)
        return res

    def get_download_url(self, browser_url):
        res = self.s.get(browser_url)
        soup = BeautifulSoup(res.text, "lxml")
        h2 = soup.find_all(attrs={"class": "carouselTitle"})[0]
        onclick = h2.a["onclick"]
        url = onclick.split("'")[1]
        download_url = "".join([url, "_yq.mp4"])
        return download_url

    def download(self, url, filename, size=None, speed=None, total=None, done=None):
        u"""
        :params :size multiprocessing Value
        """
        video = self.s.get(url, stream=True, headers={"Range": "bytes=0-"})
        content_length = video.headers["Content-Length"]
        size.value = int(content_length)
        start = time.clock()
        downloaded = 0
        log = open("E:\\temp\log.txt", "w")

        with open(filename, "wb") as f:
            per_start = time.clock()
            for chunk in video.iter_content(1024):
                per_end = time.clock()
                downloaded += 1024
                done.value = float(downloaded) / float(content_length)
                f.write(chunk)
                duration = per_end - per_start
                speed.value = 1 / duration
                per_start = time.clock()
                line = "per_end: {} per_start: {} duration: {} done: {} speed: {}\n".format(per_end, per_start, duration, done.value, speed.value)
                log.write(line)
        log.close()
        total.value = int(time.clock() - start)
        return None

from multiprocessing import Process, Value

if __name__ == "__main__":
    size = Value("i", 0)
    speed = Value("f", 0.0)
    total = Value("i", 0)
    done = Value("f", 0.0)
    url = u"""http://niczy.dgut.edu.cn:1680/course_def/res_url/L21lZGlhL2d1YW5mdS9pc2FkbWluL3h1ZWtlMS8yMS8yMDE2LzAzLTExL+m6u+ecgTogSzEy6Laj5ZGz6K++56iL77ya55S15a2mLw==@/Arduino%E7%94%B5%E8%B7%AF%E5%85%A5%E9%97%A8.flv_yq.mp4"""
    filename = "E:\\temp\\test.mp4"
    niczy = Niczy(requests.Session())
    p = Process(target=niczy.download, args=(
        url, filename, size, speed, total, done))
    p.start()
    with open("E:\\temp\download.txt", "w") as f:
        while p.is_alive():
            line = "Size:{}MB Speed: {} Done: {}% \n".format(
                size.value / 1024 / 1024, speed.value, done.value)
            print done.value
            f.writelines(line)
            time.sleep(0.2)
        line = "Size:{}MB Speed: {} Done: {}%  Total: {}\n".format(
            size.value / 1024 / 1024, speed.value, str(done.value), total.value)
        f.write(line)
    p.join()
