# _*_ coding:utf-8 _*_

import json

import requests
from bs4 import BeautifulSoup

import auth


class PhysicalClient(object):
    u""""""

    def __init__(self, session):
        self.url = "http://tyxk.dgut.edu.cn/index.php"
        self.ajax_header = {"X-Requested-With": "XMLHttpRequest"}
        self.s = session
        self.dirty_course_list = []
        self.clean_course_list = []

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

    def get_able_course(self):
        pass

    def get_result(self):
        pass

    def select(self, course_id):
        pass

    def unselect(self, course_id):
        pass

    def logout(self):
        pass

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
                res = self.s.get(self.url, params=params,
                                 timeout=4, headers=self.ajax_header)
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


for index, dirty in enumerate(tyxk.dirty_course_list):
    course_list = dirty["allCourse"]
    for course in course_list:
        course["page"] = index
        tyxk.clean_course_list.append(course)