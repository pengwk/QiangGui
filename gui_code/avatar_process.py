# _*_ coding:utf-8 _*_

import time
import os

#import wx
from PIL import Image

from teachers_info import teachers_info

# 处理体育系网站上老师大小不一的头像
# 保持原图比例

base_dir = "C:/Users/wk/OneDrive/W/QiangGui/img/"
output_dir = r"C:\Users\wk\OneDrive\W\QiangGui\img\23"

def main():
    have = 0
    lack = 0
    for teacher_name in teachers_info.iterkeys():
        print u"join 路径".encode("utf-8")
        path = os.path.join(base_dir, teacher_name + u".jpg")
        #print path.encode("utf-8")
        if os.path.isfile(path):
            have = have + 1
            #print "\n", path.encode("utf-8")
            # image = wx.Image(path)
            image = Image.open(path)
        else:
            lack = lack + 1
            print u"\n{}'s avatar doesn't exist.".format(teacher_name).encode("utf-8")
            continue

        # 保持长宽比 宽度固定 高按比例调整
        width = 200
        height = image.height / image.width * 200
    
        #scale = image.Scale(width, height, wx.IMAGE_QUALITY_BICUBIC)
        image.thumbnail((200, 300), Image.LANCZOS)
        output_name = os.path.join(output_dir, teacher_name + u".jpg")  
        # scale.SaveFile(output_name, wx.BITMAP_TYPE_JPEG)
        image.save(output_name, "JPEG")

    return have, lack

if __name__ == "__main__":
    # 计时
    start = time.clock()
    print u"\nStart at {}:".format(time.ctime())
    have, lack = main()
    end = time.clock()
    print u"\nEnd at {}\nTotal modify {} avatars use {} seconds\n{} teachers don't have avatar.".format(time.ctime(), have, end - start, lack)
