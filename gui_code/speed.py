# _*_ coding:utf-8 _*_

import threading
import multiprocessing as mp
from Queue import Queue
 
import time

from login import Physcial


if __name__ == '__main__':
    # 开始时间
    start = time.clock()
    print u'开始{}'.format(time.ctime())
    # 登录
    me = Physcial('201441302623','pwkilove5')
    me.Login()
    after_login = time.clock()
    print u'登录成功{}'.format(time.ctime())
    # 下载
    courses = me.GetAllCourse()
    print u'课程数{}'.format(len(courses))
    download = time.clock()
    print u'下载完成{}'.format(time.ctime())
    # 报告
    print u'登录用时{}'.format(after_login-start)
    print u'下载用时{}'.format(download-after_login)
    print u'总时间{}'.format(download)
    