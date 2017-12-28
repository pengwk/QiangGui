# _*_ coding:utf-8 _*_

import os
import json

import wx
import wx.grid as Grid
import wx.html
import wx.lib.buttons as GenButton
import wx.gizmos as gizmos
import wx.lib.inspection
from wx.lib.stattext import GenStaticText

from teachers_info import teachers_info

#  FindWindowByName
MyFrameNAME = "MyFrame"


class ButtonPanel(wx.Panel):

    def __init__(self, parent):
        super(ButtonPanel, self).__init__(parent, id=wx.ID_ANY, size=(-1, 20))
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hsizer)

        # 时间
        time_button = wx.ToggleButton(self, -1, u"挑时间", name=u"time_button")
        time_button.SetValue(True)
        time_button.Disable()

        # 项目
        class_button = wx.ToggleButton(self, -1, u"选课程", name=u"course_button")

        # 老师
        teacher_button = wx.ToggleButton(
            self, -1, u"找老师", name=u"teacher_button")
        #(widget, proportion, flag, border, userData)
        hsizer.AddMany([((0, 0), 1, wx.EXPAND),
                        (time_button, 0, wx.ALL, 10,),
                        (class_button, 0, wx.ALL, 10,),
                        (teacher_button, 0, wx.ALL, 10,),
                        ((0, 0), 1, wx.EXPAND)])

        # 事件绑定
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle)

    def OnToggle(self, event):
        obj = event.GetEventObject()
        button_name = obj.GetName()

        if obj.GetValue():
            # 只可以选择一个，选择另一个时自动取消
            obj.Disable()
            for name in [u"course_button", u"teacher_button", u"time_button"]:

                if name != button_name:
                    button = wx.FindWindowByName(name)
                    button.Enable()
                    button.SetValue(False)  # 取消选择

            # 更改选择面板
            self._ChangePanel(button_name)

    def _ChangePanel(self, button_name):
        # print "I need change panel for user"
        # print button_name
        button_to_panel = {u"course_button": u"course_select_panel",  # course_select_panel
                           u"teacher_button": u"teacher_select_panel",
                           u"time_button": u"time_select_panel"}

        panel = wx.FindWindowByName(u"select_panel")
        panel.ChangePanel(button_to_panel[button_name])


class SelectPanel(wx.Panel):
    u"""不显示具体内容
    """

    def __init__(self, parent, name):
        super(SelectPanel, self).__init__(
            parent, size=(900, 400), name=name)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        time_select_panel = TimeSelectPanel(self, u"time_select_panel")
        course_select_panel = CourseSelectPanel(self, u"course_select_panel")
        teacher_select_panel = TeacherSelectPanel(
            self, u"teacher_select_panel")
        do_select_panel = DoSelectPanel(self, u"do_select_panel")

        self.vsizer.AddMany([  # ((0, 0), 1, wx.EXPAND),
            (time_select_panel, 0, wx.ALL |
             wx.ALIGN_CENTER_HORIZONTAL, 5),
            (course_select_panel, 0, wx.ALL |
             wx.ALIGN_CENTER_HORIZONTAL, 5),
            (teacher_select_panel, 0, wx.ALL |
             wx.ALIGN_CENTER_HORIZONTAL, 5),
            (do_select_panel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),
            #((0, 0), 1, wx.EXPAND),
        ])

        wx.FindWindowByName(u"course_select_panel").Hide()
        wx.FindWindowByName(u"teacher_select_panel").Hide()
        wx.FindWindowByName(u"do_select_panel").Hide()

        self.SetSizer(self.vsizer)

    def ChangePanel(self, panel_name):
        self.Freeze()
        widget_names = [u"course_select_panel",
                        u"time_select_panel",
                        u"teacher_select_panel",
                        u"do_select_panel"]

        for widget_name in widget_names:
            if widget_name == panel_name:
                wx.FindWindowByName(widget_name).Show()
                self.GetParent().Layout()
            else:
                self.vsizer.Hide(wx.FindWindowByName(widget_name))

                # wx.FindWindowByName(widget_name).Hide()
                # self.vsizer.Layout()
                self.GetParent().Layout()
        self.Thaw()


class FilterPanel(wx.Panel):

    def __init__(self, parent):
        super(FilterPanel, self).__init__(parent, size=(900, 200))
        self.list = CourseResultList(self, u"course_result_list")

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        align = wx.ALIGN_CENTER
        self.vsizer.Add(self.list, 1, align)
        self.SetSizer(self.vsizer)


class CourseResultList(wx.ListCtrl):
    u"""课程选择结果列表"""

    def __init__(self, parent, name):
        style = wx.LC_REPORT
        super(CourseResultList, self).__init__(parent, name=name, style=style)
        self.InsertColumn(0, u"周几")
        self.InsertColumn(1, u"节次")
        self.InsertColumn(2, u"老师")
        self.InsertColumn(3, u"课程名")
        # 课程数据
        self.fake_course = {0: u"周一",
                            1: u"五六节",
                            2: u"苏发韧",
                            3: u"羽毛球"}

        self.AddRow(0, self.fake_course)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        # self.Bind(wx.EVT_LIST_DESELECT, self.OnSelect)

    def AddRow(self, row, course_data):
        self.InsertStringItem(0, u"")
        for col in range(0, 4):
            label = course_data[col]
            self.SetStringItem(row, col, label)
        return None

    def OnSelect(self, event):
        u"""处理课程选择事件，删除选择课程，更新到DoSelectPanel"""
        select_panel = wx.FindWindowByName(u"select_panel")
        select_panel.ChangePanel(u"do_select_panel")

        do_select_panel = wx.FindWindowByName(u"do_select_panel")
        do_select_panel.AddCourse(None)

        return None


class DoSelectPanel(wx.Panel):
    u"""最后显示选择结果的，退选、的面板"""

    def __init__(self, parent, name):
        super(DoSelectPanel, self).__init__(parent, name=name)
        self.course_count = 0

        self.msizer = wx.GridBagSizer(vgap=10, hgap=5)
        # self.MakeSelectingCourse(None)
        self.SetSizer(self.msizer)

    def AddCourse(self, course):
        if self.course_count == 0:
            self.MakeSelectingCourse(None)
            self.course_count += 1
            pass
        elif self.course_count <= 2:
            self.MakeSelectingCourse(None)
            self.course_count += 1
            pass
        elif self.course_count <= 4:
            self.MakeSelectingCourse(None)
            self.course_count += 1
            pass
        elif self.course_count > 4:
            self.MakeSelectingCourse(None)
            self.course_count += 1
            pass
        return None

    def MakeSelectingCourse(self, course_data):
        course_widget = None
        index_label = unicode(self.course_count + 1)
        index = wx.StaticText(self, label=index_label)

        course_label = u"周一 七八节 苏发韧 羽毛球"
        course = wx.StaticText(self, label=course_label)

        button = GenButton.GenButton(self, label=u"自动开始")
        cancel_button = GenButton.GenButton(
            self, label=u"取消", style=wx.BORDER_NONE)

        row = self.course_count + 1
        self.msizer.AddMany([(index, (row, 0), (1, 1), wx.ALIGN_CENTER),
                             (course, (row, 1), (1, 1), wx.ALIGN_CENTER),
                             (button, (row, 2), (1, 1), wx.ALIGN_CENTER),
                             (cancel_button, (row, 3), (1, 1), wx.ALIGN_CENTER)])
        # self.msizer.Layout()
        self.GetParent().Layout()
        return course_widget

    def MakeSpareCourse(self, course_data):
        u"""Spare备用"""
        course_widget = None
        return None

# 具体选择的面板


class TimeSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TimeSelectPanel, self).__init__(
            parent, name=name,)

        # self.SetBackgroundColour("red")

        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.time_grid = TimeGrid(self, u"time_grid")
        self.vsizer.Add(self.time_grid, 0, wx.EXPAND)
        self.SetSizer(self.vsizer)


class TimeGrid(Grid.Grid):
    u""""""

    def __init__(self, parent, name):
        super(TimeGrid, self).__init__(parent, name=name)

        # bug
        self.counter = 0

        self.EnableEditing(False)  # 禁止编辑
        self.DisableDragGridSize()  # 禁止在网格区缩放表格
        self.DisableDragRowSize()  # 禁止在行标题区拉伸表格
        self.DisableDragColSize()  # 禁止在列标题区拉伸网格
        self.SetSelectionBackground(
            (255, 255, 255))  # 选择前景色为白色 看不见拖拽选择
        self.SetCellHighlightPenWidth(0)  # 去掉单击高亮时显示的框

        self.Bind(Grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelClick)
        self.Bind(Grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(Grid.EVT_GRID_CELL_LEFT_CLICK,
                  self.OnCellLeftClick)

        sections = [u"一、二", u"三、四", u"五、六", u"七、八"]  # 节
        days = [u"一", u"二", u"三", u"四", u"五"]  # 星期几

        row_count = len(days)
        col_count = len(sections)
        self.CreateGrid(row_count, col_count)

        # 显示星期几
        for row, num_cn in enumerate(days):
            self.SetRowLabelValue(row, u"星期{}".format(num_cn))
        # 显示第几节
        for col, num_cn in enumerate(sections):
            self.SetColLabelValue(col, u"第{}节".format(num_cn))

        # 表格大小
        width = 800 / col_count
        height = 300 / row_count
        self.SetDefaultColSize(width)
        self.SetDefaultRowSize(height)

    def OnLabelClick(self, event):
        u"""阻止用户点击标签栏，选择整行或整列"""
        event.Veto()

    def OnRangeSelect(self, event):
        u"""看不见鼠标拖动选择"""
        if self.GetSelectionBlockTopLeft() == self.GetSelectionBlockBottomRight():
            pass
        else:
            self.ClearSelection()
            self.counter = self.counter + 1
            print "clear selection{}".format(self.counter)

    def OnCellLeftClick(self, event):
        u""""""
        print "CellClick"

        row = event.GetRow()
        col = event.GetCol()

        selected_color = wx.Colour(8, 195, 105)
        white = wx.Colour(255, 255, 255)
        old_color = self.GetCellBackgroundColour(row, col)
        # 取消选择
        if old_color == selected_color:  # 红色
            self.SetCellBackgroundColour(row, col, white)
        else:
            self.SetCellBackgroundColour(row, col, selected_color)
        self.Refresh()


class CourseSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(CourseSelectPanel, self).__init__(
            parent, name=name)
        # bug
        # self.SetBackgroundColour("blue")

        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)

        course_list = [u"篮球.jpg", u"健美.jpg", u"健身.jpg", u"排球.jpg", u"武术.jpg", u"游泳.jpg",
                       u"足球.jpg", u"羽毛球.jpg", u"瑜伽.jpg", u"健美操.jpg", u"网球.jpg", u"乒乓球.jpg", ]
        img_dir = "C:\Users\pengw\OneDrive\W\QiangGui\img"

        for course in course_list:
            bmp = wx.Image(os.path.join(img_dir, course)).ConvertToBitmap()
            course_button = GenButton.GenBitmapToggleButton(self, -1, bmp)
            course_button.SetBitmapSelected(bmp)
            self.vsizer.Add(course_button, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.vsizer)


class TeacherSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TeacherSelectPanel, self).__init__(
            parent, name=name)
        # bug
        # self.SetBackgroundColour("gray")
        # 添加老师姓名
        self.hsizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        for index, teacher_name in enumerate(teachers_info.iterkeys()):
            if index <= 8:
                button = wx.ToggleButton(self, label=teacher_name)
                self.hsizer_1.Add(button, 1, wx.EXPAND | wx.ALL, 5)
            elif index <= 17:
                button = wx.ToggleButton(self, label=teacher_name)
                self.hsizer_2.Add(button, 1, wx.EXPAND | wx.ALL, 5)
            elif index <= 26:
                button = wx.ToggleButton(self, label=teacher_name)
                self.hsizer_3.Add(button, 1, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle)

        # 老师信息
        self.info_sizer = wx.BoxSizer()
        self.info_panel = TeacherInfoPanel(self, u"teacher_info_panel")
        self.info_sizer.Add(self.info_panel, 0, wx.EXPAND)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.AddMany([(self.hsizer_1, 0, wx.EXPAND),
                             (self.hsizer_2, 0, wx.EXPAND),
                             (self.hsizer_3, 0, wx.EXPAND),
                             (self.info_sizer, 1, wx.EXPAND)])
        self.SetSizer(self.vsizer)

    def OnToggle(self, event):
        button = event.GetEventObject()
        print "OnToggle"
        print button.GetValue()
        self.info_panel.RefreshInfo(button.GetLabel())
        if button.GetValue():
            # 加入筛选条件
            pass
        else:
            # 删除筛选条件
            print "pass"
            pass


class TeacherInfoPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TeacherInfoPanel, self).__init__(parent, name=name)
        self.hsizer = None

        # self.OnToggle()

    def RefreshInfo(self, name):
        # debug
        print "Refresh", name.encode("utf-8")
        self.Freeze()
        if self.hsizer == None:
            self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
            self.SetSizer(self.hsizer)
        else:
            items = self.Children
            [item.Destroy() for item in items]
            # self.hsizer.Clear()
            self.hsizer.Layout()
        # avatar 意为头像
        img_dir = r"C:\Users\pengw\OneDrive\W\QiangGui\img\avatar"
        path = os.path.join(img_dir, name + u".jpg")
        bmp = wx.Image(path).ConvertToBitmap()
        avatar = wx.StaticBitmap(self, bitmap=bmp)
        self.hsizer.Add(avatar, 1, wx.ALIGN_LEFT | wx.ALL, 5)

        # 文字部分
        teacher = teachers_info[name]

        # 名字 职称
        name_title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = u"名字：" + name
        label_2 = u"职称：" + teacher[u"title"]
        name_title_sizer.AddMany([(wx.StaticText(self, label=label_1, size=(200, -1)), 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALIGN_CENTER | wx.ALL, 5),
                                  (wx.StaticText(self, label=label_2, size=(200, -1)), 1, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 5)])
        # 年月 性别
        birth_gender_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = u"出身年月：" + teacher[u"birthday"]
        label_2 = u"性别：" + teacher[u"gender"]
        birth_gender_sizer.AddMany([(wx.StaticText(self, label=label_1, size=(200, -1)), 0, wx.EXPAND | wx.ALL, 5),
                                    (wx.StaticText(self, label=label_2, size=(200, -1)), 0, wx.EXPAND | wx.ALL, 5)])
        # 毕业院校
        label = u"毕业院校：" + teacher[u"graduated_school"]
        graduated_school = wx.StaticText(
            self, label=label)
        # 研究方向
        label = u"研究方向：" + teacher[u"research"]
        research = wx.StaticText(self, label=label)

        self.intro = wx.StaticText(self, label=teacher[u"intro"])

        statement = u"信息源于http://tyx.dgut.edu.cn/szdw/index.jhtml"
        self.statement = wx.StaticText(self, label=statement)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.AddMany([(name_title_sizer, 1, wx.ALL, 5),
                             (birth_gender_sizer, 1, wx.ALL, 5),
                             (graduated_school, 1, wx.ALL, 5),
                             (research, 1, wx.ALL, 5),
                             (self.intro, 1, wx.ALL | wx.EXPAND, 5),
                             (self.statement, 1, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM), ])

        self.hsizer.Add(self.vsizer, 2, wx.EXPAND)
        self.hsizer.Layout()
        self.GetParent().info_sizer.Layout()
        self.Thaw()

class AboutDialog(wx.Dialog):
    u""""""

    def __init__(self, parent, name, title):
        style = wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE
        super(AboutDialog, self).__init__(
            parent, name=name, style=style, title=title)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        about_panel = AboutPanel(self, u"about_panel")
        flags = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER
        self.vsizer.Add(about_panel, 0, flags, 30)

        self.SetSizerAndFit(self.vsizer)


class AboutPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        size = (-1, -1)  # (300, 400)
        super(AboutPanel, self).__init__(parent, name=name, size=size)

        self.gbsizer = wx.GridBagSizer(vgap=5, hgap=5)

        img_dir = "C:\Users\pengw\OneDrive\W\QiangGui\img"
        path = os.path.join(img_dir, "wechat200.jpg")
        image = wx.Image(path).ConvertToBitmap()

        wechat_text = wx.StaticText(self, label=u"微信/WeChat：")
        wechat_bmp = wx.StaticBitmap(self, bitmap=image)

        mail_text = wx.StaticText(self, label=u"邮箱/Mail：")
        mail_addr = wx.StaticText(self, label=u"pengwk2@gmail.com")

        author_text = wx.StaticText(self, label=u"作者/Author：")
        author_name = wx.StaticText(self, label=u"彭未康")

        school_msg = u"""不知道会不会影响你们的工作，如果给您添麻烦了，抱歉！\n """
        to_school = wx.StaticText(self, label=school_msg)
        school_text = wx.StaticText(self, label=u"网站管理：")

        teacher_msg = u"""证件照和介绍信息是体育系官网找到的，抱歉！如果老师愿意提供靓照，感激不尽。\n """
        to_teacher = wx.StaticText(self, label=teacher_msg)
        teacher_text = wx.StaticText(self, label=u"亲爱的老师：")

        others_msg = u"""希望能帮到你，有什么想法或问题加我微信聊，邮箱也没问题。\n \n """
        to_others = wx.StaticText(self, label=others_msg)
        others_text = wx.StaticText(self, label=u"同学、朋友：")

        # 版权声明
        copyright_text = wx.StaticText(self, label=u"版权声明：")
        copyright = wx.StaticText(self, label=u"保留所有权利。")

        self.gbsizer.AddMany([(school_text, (0, 0)),
                              (to_school, (0, 1)),

                              (teacher_text, (1, 0)),
                              (to_teacher, (1, 1)),

                              (others_text, (2, 0)),
                              (to_others, (2, 1)),

                              (author_text, (3, 0)),
                              (author_name, (3, 1)),

                              (mail_text, (4, 0)),
                              (mail_addr, (4, 1)),

                              (wechat_text, (5, 0)),
                              (wechat_bmp, (5, 1)),

                              (copyright_text, (7, 0)),
                              (copyright, (7, 1)),
                              ])

        self.SetSizer(self.gbsizer)


class LoginDialog(wx.Dialog):
    u""""""

    def __init__(self, parent, name, title):
        super(LoginDialog, self).__init__(parent, name=name, title=title)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.login_panel = LoginPanel(self)
        flags = wx.EXPAND | wx.ALIGN_CENTER 
        self.main_sizer.Add(self.login_panel, 1, flags| wx.ALL, 20)
        self.SetSizerAndFit(self.main_sizer)

    def GetAccount(self):
        return self.login_panel.GetAccount()

    def CheckPassword(self):
        self.ShowModal()
        if self.login_panel.CheckPassword() == False:
            self.SetTitle(u"密码错误")

            self.CheckPassword()
        else:
            return True

class LoginPanel(wx.Panel):
    u""""""
    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent)

        self.gbsizer = wx.GridBagSizer(vgap=5, hgap=5)

        self.student_id_label = wx.StaticText(self, label=u"学号：")
        self.student_id_text = wx.TextCtrl(self,)
        self.password_label = wx.StaticText(self, label=u"密码：")
        self.password_text = wx.TextCtrl(self, style=wx.TE_PASSWORD)

        self.check_button = wx.Button(self, wx.ID_OK, u"登录")
        self.check_button.SetDefault()

        self.gbsizer.AddMany([(self.student_id_label, (0, 0), (1, 1), wx.ALIGN_CENTER|wx.ALL,),
                              (self.student_id_text, (0, 1), (1, 1), wx.ALIGN_CENTER|wx.ALL,),

                              (self.password_label, (1, 0), (1, 1), wx.ALIGN_CENTER|wx.ALL,),
                              (self.password_text, (1, 1), (1, 1), wx.ALIGN_CENTER|wx.ALL,),
                              (self.check_button, (2, 1))
                              ])

        self.SetSizerAndFit(self.gbsizer)

    def CheckPassword(self,):
        account = self.GetAccount()
        if account["student_id"] == "1":
            return True
        else:
            return False

    def GetAccount(self):
        account = {}

        account[u"student_id"] = self.student_id_text.GetValue()
        account[u"password"] = self.password_text.GetValue()

        return account

class TopStatesBar(wx.Panel):
    u"""窗口顶部 登录，退出，显示网络状态，联系作者"""

    def __init__(self, parent, name):
        style = 0
        super(TopStatesBar, self).__init__(parent, name=name, style=style)

        # 登录
        # login_bmp = wx.Image(path).ConvertToBitmap()
        login = GenButton.GenButton(
            self, label=u"登录", size=(-1, 18), style=wx.BORDER_NONE)
        # login = GenStaticText(self, label=u"登录")
        self.Bind(wx.EVT_BUTTON, self.OnClick, login)
        # 网络状态 在线 内网 外网
        online = wx.StaticText(self, label=u"在线")
        internet = GenButton.GenButton(
            self, label=u"外网", size=(-1, 18), style=wx.BORDER_NONE)
        image = wx.Image("C:\Users\pengw\OneDrive\W\QiangGui\img\yellow.png").ConvertToBitmap()
        internet_bmp = wx.StaticBitmap(self, bitmap=image)
        intranet = wx.StaticText(self, label=u"内网")
        image = wx.Image(
            r"C:\Users\pengw\OneDrive\W\QiangGui\img\red.png").ConvertToBitmap()
        intranet_bmp = wx.StaticBitmap(self, bitmap=image)
        image = wx.Image(
            r"C:\Users\pengw\OneDrive\W\QiangGui\img\green.png").ConvertToBitmap()
        green_bmp = wx.StaticBitmap(self, bitmap=image)
        # 选课开始时间 倒计时
        time = wx.StaticText(self, label=u"倒计时")
        led = gizmos.LEDNumberCtrl(self, size=(-1, 18))
        led.SetValue("1-33-23")
        # led.SetForegroundColour("red")
        # 联系作者 文字加弹窗
        author = GenButton.GenButton(
            self, label=u"联系作者", style=wx.BORDER_NONE, size=(-1, 18))
        self.Bind(wx.EVT_BUTTON, self.OnAbout, author)

        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.AddMany([(login, 0, wx.LEFT | wx.RIGHT, 5),
                             (online, 0, wx.RIGHT, 5),
                             (green_bmp, 0, wx.RIGHT | wx.ALIGN_CENTER, 5),
                             (internet, 0, wx.RIGHT, 5),
                             (internet_bmp, 0, wx.RIGHT | wx.ALIGN_CENTER, 5),
                             (intranet, 0, wx.RIGHT, 5),
                             (intranet_bmp, 0, wx.RIGHT | wx.ALIGN_CENTER, 5),
                             (time, 0, wx.RIGHT, 5),
                             (led, 0, wx.RIGHT, 5),
                             ((0, 0), 1, wx.EXPAND),
                             (author, 0, wx.RIGHT | wx.ALIGN_RIGHT, 5),
                             ])
        self.SetSizer(self.hsizer)

    def OnClick(self, event):
        dlg = LoginDialog(self, u"login_dialog", u"登录")
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            if dlg.CheckPassword():
                # 密码正确
                account = dlg.GetAccount()
                print account
                # 调用登录
                dlg.Destroy()
            
        
        

    def OnAbout(self, event):
        dlg = AboutDialog(self, u"about_dialog", u"联系作者")
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()


class MyFrame(wx.Frame):

    def __init__(self, parent, id, title, pos, size, style, name):
        super(MyFrame, self).__init__(
            parent, id, title, pos, size, style, name)
        #self.panel = wx.Panel(self)

        # 布局
        self._DoLayOut()

        # toolbar = TopToolBar(self, u"top_tool_bar")
        # self.SetToolBar(toolbar)

    def _DoLayOut(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vsizer)

        vsizer.AddMany([(TopStatesBar(self, u"top_states_bar"), 0, wx.EXPAND),
                        (FilterPanel(self), 1, wx.ALL |
                         wx.ALIGN_CENTER_HORIZONTAL, 5),
                        (SelectPanel(self, u"select_panel"), 1, wx.ALL |
                         wx.ALIGN_CENTER_HORIZONTAL, 5),
                        (ButtonPanel(self), 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)])


class MyApp(wx.App):

    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, u"优选课", wx.DefaultPosition,
                             (1000, 750), wx.DEFAULT_FRAME_STYLE, MyFrameNAME)

        #size = self.frame.GetBestSize()
        # self.frame.SetSize(size)
        # wx.Log.SetLogLevel(0)

        self.SetTopWindow(self.frame)

        # inspection 工具
        wx.lib.inspection.InspectionTool().Show()

        self.frame.Show()
        self.frame.Center()
        # 修复时间选择启动不显示
        self.frame.Layout()
        return True

if __name__ == "__main__":
    app = MyApp(redirect=False, useBestVisual=True)
    app.MainLoop()
