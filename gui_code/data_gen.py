# _*_ coding:utf-8 _*_

import json
import random
# 生成课程数据
# 要求： 各不相同
# 例子：
# {"course_id":1, "name":u"孙吴莹", "course_name":u"健身健美", "time":u"下午三四节", "day":u"周三", "campus":u"松山湖", "place":u"篮球场", "capacity":u"23", "selectedman":u"23", "able":u"1", "sex_limit":u"无" }

# 时间节数表
course_time_ = {"1": (u"第一节", ("8:30", "9:15")),
               "2": (u"第二节", ("9:25", "10:10")),
               "3": (u"第三节", ("10:25", "11:10")),
               "4": (u"第四节", ("11:15", "12:00")),
               "5": (u"第五节", ("14:30", "15:15")),
               "6": (u"第六节", ("15:25", "16:10")),
               "7": (u"第七节", ("16:25", "17:10")),
               "8": (u"第八节", ("17:20", "18:05")),
               "9": (u"第九节", ("19:30", "20:15")),
               "10": (u"第十节", ("20:25", "21:10")),
               "11": (u"第十一节", ("21:15", "22:00")),
               "0": (u"早读", ("7:50", "8:20"))}

course_time = {"1": (u"第一节", (u"8:30-9:15", )),
               "2": (u"第二节", (u"9:25-10:10", )),
               "3": (u"第三节", (u"10:25-11:10", )),
               "4": (u"第四节", (u"11:15-12:00", )),
               "5": (u"第五节", (u"14:30-15:15", )),
               "6": (u"第六节", (u"15:25-16:10", )),
               "7": (u"第七节", (u"16:25-17:10", )),
               "8": (u"第八节", (u"17:20-18:05", )),
               "9": (u"第九节", (u"19:30-20:15", )),
               "10": (u"第十节", (u"20:25-21:10", )),
               "11": (u"第十一节", (u"21:15-22:00", )),
               "0": (u"早读", (u"7:50-8:20", ))}

teacher_name = (u"胡伟超", u"马陈飞", u"吴坤峰",
                u"周林群", u"周炽杰", u"郑智勇",
                u"招鸿明", u"张艺惠", u"张华杰",
                u"张柏仲", u"袁契天", u"叶伟权",
                u"叶翰铭", u"杨天生", u"杨飞文",
                u"徐振杰", u"谢瑞根", u"吴志杰",
                u"吴育洪", u"吴泰宇", u"吴寿宏",
                u"温汉杰", u"韦峰强", u"涂腾达",
                u"丘富津", u"麦芷莹", u"刘檀华",
                u"刘丹红", u"林煜",   u"林泽彬",
                u"林景德", u"林佳纯", u"梁思远",
                u"练威赞", u"李星",   u"李晓亮",
                u"李土源", u"李梅娟", u"李承锠",
                u"赖敏华", u"黄茵茵", u"黄东海",
                u"何沛聪", u"何光宝", u"陈芷君",
                u"陈铭",   u"陈华辉", u"陈恩科",
                u"曹欢贤", u"蔡楚镐", u"蔡彬",
                u"朱仕淦", u"朱进礼", u"张舒",
                u"张绍雄", u"张霖琳", u"张发杰",
                u"余子良", u"杨长城", u"徐境敏",
                u"谢家驹", u"萧裕恒", u"吴子煜",
                u"王再华", u"王伟谦", u"唐肇阳",
                u"苏倩",   u"苏学法", u"苏桂丹",
                u"苏富文", u"彭未康", u"莫家乐",
                u"麦康福", u"刘志江", u"林钺清",
                u"林一钧", u"梁洲",  u"梁广进",
                u"黎浩鹏", u"黎博雄", u"江锦涛",
                u"黄丽强", u"黄镜鸿", u"黄国锋",
                u"胡学斌", u"何向东", u"郭晓",
                u"高伟强", u"冯敏",  u"陈炜强",
                u"陈莹",  u"陈小盈", u"陈晓茹",
                u"陈浩驹", u"陈彩瑜", )

teachers = (u"曹永强", u"张前锋", u"冯炎红",
            u"陈丹丹", u"刘明", u" 黎荣",
            u" 廖国君", u"曾志和", u"苏敷志",
            u"包丽华", u"胡英姿", u"刘琪",
            u"孙吴莹", u"胡古玥", u"吴伟锋",
            u"肖卫", u"张维达", u"梁凡",
            u"李朝霞", u"沈放", u"高峰",
            u"李逸涛", u"潘荣远", u"张恒",
            u"赵 全", u"刘宏宇", u"陈进",
            u"张一", u"王二", u"黄三",)


course_name = (u"篮球", u"排球", u"羽毛球",
               u"乒乓球", u"足球", u"网球",
               u"健身健美", u"瑜伽", u"武术",
               u"体育游戏", u"健美操", u"游泳",)

weeks = (u"星期一", u"星期二", u"星期三", u"星期四", u"星期五", )

campuses = (u"松山湖", u"莞城", )

places = (u"足球场", u"假草", u"真草", u"器材室", u"舞蹈室", u"篮球场", )

dir_ = r"C:\Users\wk\OneDrive\W\QiangGui\temp"

course_template = {"course_id": "",
                   "name": "",
                   "course_name": "",
                   "time": "",
                   "day": "",
                   "campus": "",
                   "place": "",
                   "capacity": "",
                   "selectedman": "",
                   "able": "",
                   "sex_limit": ""}

# 最后才添加 course_id




def two_times():
    ints = [str(random.randint(5, 8))]
    second = str(random.randint(5, 8))
    while second  in ints:
        second = str(random.randint(5, 8))
        break
    ints.append(second)
    times = [course_time[No][1] for No in ints]
    return times

def gen_all_course():
    courses = []
    course_index = range(12)*3 
    for index, teacher in enumerate(teachers):
        for week in weeks:
            for time_ in two_times():
                course = {}
                course[u"course_name"] = course_name[course_index[index]]
                course[u"name"] = teacher
                course[u"time"] = time_
                course[u"day"] = week
                courses.append(course)
    for index, course in enumerate(courses):
        course[u"course_id"] = index
        course[u"campus"] = random.choice(campuses) 
        course[u"place"] = random.choice(places)
        course[u"capacity"] = random.randint(20, 30)
        course[u"selectedman"] = random.randint(0, 30)
        course[u"able"] = random.randint(0, 1)
        course[u"sex_limit"] = random.randint(0, 1)
    print len(courses)
    return courses

def course_gen(count):
    data = []
    for course_id in xrange(1, count + 1):
        if len(data) == count:
            return data
        else:
            while True:
                course = one_course()
                if course not in data:
                    course["course_id"] = course_id
                    course["campus"] = random.choice(campuses) 
                    course["place"] = random.choice(places)
                    course["capacity"] = random.randint(20, 30)
                    course["selectedman"] = random.randint(0, 30)
                    course["able"] = random.randint(0, 1)
                    course["sex_limit"] = random.randint(0, 1)
                    data.append(course)
                    break
    return data


def save_to_json(filename, data):
    with open(dir_ + filename, "w") as f:
        # f.write(json.dumps(data))
        json.dump(data, f)
    return None

if __name__ == '__main__':
    course_count = 300
    save_to_json("course_data.json", gen_all_course())
