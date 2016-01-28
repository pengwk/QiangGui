# _*_ coding:utf-8 _*_

# 图像 --- 字符串
# 
# 
import wx
import os

def convert(path):
    # load 
    # get image name 
    fullname = os.path.split(path)[1]
    name = os.path.splitext(fullname)[0]

    name = {"name":name,
            "Data":"",
            "Width":"",
            "Height":""}
    img = wx.Image(path)
    name['Width'] = img.GetWidth()
    name['Height'] = img.GetHeight()
    name['Data'] = img.GetData()
    return name


def save(path,imglist):
    # 文件名
    # os.path.basename(path)
    # 连接成路径
    # os.path.join(,name + '.py')
    # 后缀名与文件名分开
    # os.path.splitext(path)
    # os.path.basename("D:/pengwk/myproject/qiang.py")
    # 'qiang.py'
    # os.path.splitext("D:/pengwk/myproject/qiang.py")
    # ('D:/pengwk/myproject/qiang', '.py')
    with open(path,'a') as imgfile:
        imgfile.writelines("# _*_ coding:utf-8 _*_\n")
        imgfile.writelines("#!/usr/bin/env python\n")
        imgfile.writelines("\n")
        for img in imglist:
            imgfile.writelines(img + "Width " + "= " + img[Width] + '\n')
            imgfile.writelines(name + "Height " + "= " + img[Height] + '\n')
            imgfile.writelines(name + "Str " + "= " + img[Data] + '\n')

if __name__ == "__main__":
    # 需要转换的文件列表
    imageList = ['./']
    # 获取完整路径
    imagePath = [os.path.abspath(img) for img in imageList]
    # 转换
    converted = [convert(img) for img in imageList]
    # 写进文件
    save()