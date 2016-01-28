# _*_ coding:utf-8 _*_
#!/usr/bin/env python

import wx
import os
from LoginDialog import LoginDialog
from login import Physcial

user = None


class InfoPanel(wx.Panel):

    """docstring for InfoPanel"""

    def __init__(self, parent):
        super(InfoPanel, self).__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.login_btn = wx.Button(self, -1, u'请登录')
        self.Bind(wx.EVT_BUTTON, self.login, self.login_btn)
        self.sizer.Add(self.login_btn, 0, wx.ALL, 0)
        self.SetSizer(self.sizer)

    def login(self, event):
        global user
        dlg = LoginDialog(None, -1, u'请登录')
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            self.change('n')
            # user = Physcial(dlg.GetUsername(),dlg.GetPassword())
            # try:
            #      user.newlogin()
            # except ValueError:
            #      pass

    def change(self, event):
        # self.Destroy(self.login_btn)
        self.login_btn.Destroy()
        self.username = wx.StaticText(self, -1, '201441302623')
        self.name = wx.StaticText(self, -1, u'彭未康')
        self.btn = wx.Button(self,-1,u'切换账号')
        self.Bind(wx.EVT_BUTTON,self.change_user,self.btn)
        self.sizer.AddMany([(self.name, 0, wx.EXPAND | wx.ALL, 10),
                           (self.username, 0, wx.EXPAND | wx.ALL, 10),
                           (wx.StaticText(self,-1,u"2014通信六班"),0,wx.ALIGN_CENTER_VERTICAL|wx.EXPAND | wx.ALL, 10),
                           (self.btn,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)])
        self.SetSize(self.GetBestSize())
        self.SetAutoLayout(True)
        self.sizer.Layout()
        self.Refresh()
    def change_user(self,event):
        global user
        print 'change user'

class CoursePanel(wx.Panel):

    """已选的可以退选，从筛选区选择的"""

    def __init__(self, parent, label,btnlabel):
        super(CoursePanel, self).__init__(parent)
        self.sbox = wx.StaticBox(self, -1, label=label)
        sboxsizer = wx.StaticBoxSizer(self.sbox, wx.HORIZONTAL)
        # sboxsizer.Add(wx.StaticText(self,-1,u'尚未选择'),0,wx.ALL,0)
        catalogs = [u'老师', u'地点', u'周几', u'校区', u'时间', u'种类']
        for catalog in catalogs:
            sboxsizer.Add(wx.StaticText(self, -1, catalog), 0, wx.RIGHT, 60)
        self.btn = wx.Button(self,-1,btnlabel)
        self.Bind(wx.EVT_BUTTON,self.change,self.btn) 

        sboxsizer.Add(self.btn, 0, wx.RIGHT, 60)
        msizer = wx.BoxSizer(wx.HORIZONTAL)
        msizer.Add(sboxsizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(msizer)
    def change(self,event):
        global user
        btn = event.GetEventObject()
        if btn.GetLabel() == u'退选':
            print '退选'
        elif btn.GetLabel() == u"开抢":
            print '开抢'
        else:
            print "Error"
        


class MainPanel(wx.Panel):

    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)
        self.SetAutoLayout(True)
        # 登陆模块
        self.userinfo = InfoPanel(self)
        self.selected = CoursePanel(self, u'已选',u'退选')
        self.wanted = CoursePanel(self, u'想选',u'开抢')
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.userinfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND | wx.ALL, 10)
        vsizer.Add(self.selected, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND | wx.TOP, 5)
        vsizer.Add(self.wanted, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND | wx.TOP, 5)

        # 筛选模块
        self.filterAera(vsizer)
        # 筛选结果
        self.resultList(vsizer)

        # 抢课模块
        # self.qiang(vsizer)

        # 支持作者模块
        # self.supportAuthor(vsizer)

        self.SetSizer(vsizer)

    def supportAuthor(self, sizer):
        '''
        支持作者模块
        '''
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        WeixinPayImage = wx.Image(
            './WeixinPay.bmp', wx.BITMAP_TYPE_BMP).Scale(250, 250)
        AliPayImage = wx.Image(
            './AliPay1.bmp', wx.BITMAP_TYPE_BMP).Scale(250, 250)
        print "weixin", WeixinPayImage.GetWidth(),\
            WeixinPayImage.GetHeight()
        print "AliPay", AliPayImage.GetWidth(),\
            AliPayImage.GetHeight()
        WeixinPay = wx.StaticBitmap(
            self, bitmap=WeixinPayImage.ConvertToBitmap())
        AliPay = wx.StaticBitmap(self, bitmap=AliPayImage.ConvertToBitmap())
        hsizer.Add(WeixinPay, 0.5, wx.ALL, 10)
        hsizer.Add(AliPay, 0, wx.ALL, 10)

        sizer.Add(hsizer, 0, wx.EXPAND)

    def qiang(self, sizer):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        selected = wx.StaticText(self, -1, u"已选择课程")
        hsizer.Add(selected, 0, wx.ALL, 10)
        button = wx.Button(self, -1, u"抢！")
        hsizer.Add(button, 0, wx.ALL, 10)
        sizer.Add(hsizer, 0, wx.EXPAND)

    def resultList(self, sizer):
        catalogs = [u'老师', u'地点', u'周几', u'校区', u'时间', u'种类']
        showList = wx.ListCtrl(self, style=wx.LC_REPORT)
        for catalog in catalogs:
            index = 0
            showList.InsertColumn(index, catalog)
            index += 1
        sizer.Add(showList, 0, wx.ALL, 10)

    def filterAera(self, sizer):
        '''筛选按钮'''
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        catalogs = [u'老师', u'地点', u'周几', u'校区', u'时间', u'种类']
        for catalog in catalogs:
            teacherList = [u"彭未康", u"彭贵洪", u"彭未阳"]
            dropdown = wx.ComboBox(
                self, -1, catalog, (15, 20), wx.DefaultSize, teacherList, wx.CB_DROPDOWN)
            hsizer.Add(dropdown, 0, wx.ALL, 15)
        sizer.Add(hsizer, 0, wx.EXPAND)


class MyFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY,
                 title=u"主框架",
                 name="MyFrame",
                 pos=wx.DefaultPosition,
                 size=(1000, 700),
                 style=wx.DEFAULT_FRAME_STYLE):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)
        self.Center()
        # size 的位置要与前面的相对应
        self.panel = MainPanel(self)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(vsizer)
        # 菜单
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.NewId(), u"作者", u'联系我')
        menuBar.Append(menu, u"&联系作者")
        self.SetMenuBar(menuBar)

        # 标题栏/系统托盘 图标

        self.TitleIcon()

        # 状态栏
        # Todo 自定义 添加控件
        self.CreateStatusBar()

    def TitleIcon(self, image="./pengwk.ico"):
        """暂只支持*.ico"""
        # 添加菜单事件响应
        path = os.path.abspath(image)
        print path
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 系统托盘图标
        # taskicon = wx.TaskBarIcon()
        # taskicon.SetIcon(icon)


class MyApp(wx.App):

    def OnInit(self):
        # Todo icon
        # 启动画面
        import wx
        img = wx.Bitmap('AliPay.bmp')
        wx.SplashScreen(img, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT, 0,
                        parent=None, id=-1)
        wx.Yield()
        # 框架
        self.frame = MyFrame(None, title=u"抢课啦！")
        size = self.frame.GetBestSize()
        self.frame.SetSize(size)
        self.SetTopWindow(self.frame)
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
        self.frame.Show()

        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
