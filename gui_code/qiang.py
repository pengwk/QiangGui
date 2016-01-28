# _*_ coding:utf-8 _*_
#!/usr/bin/env python

import wx
import wx.lib.inspection
import os
from LoginDialog import LoginDialog
from login import Physcial

User = None


class InfoPanel(wx.Panel):

    """docstring for InfoPanel"""

    def __init__(self, parent):
        super(InfoPanel, self).__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.login_btn = wx.Button(self, -1, u'请登录')
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.login_btn)
        self.sizer.Add(self.login_btn, 0, wx.ALL, 0)
        self.SetSizer(self.sizer)

    def OnButton(self, event):
        global User
        dlg = LoginDialog(None, -1, u'请登录')
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            User = dlg.GetUser()
            print User
            self.change('n')
            dlg.Destroy()
            # user = Physcial(dlg.GetUsername(),dlg.GetPassword())
            # try:
            #      user.newlogin()
            # except ValueError:
            #      pass

    def change(self, event):
        global User
        print User
        # self.Destroy(self.login_btn)
        userinfo = User.GetUserInfo()
        self.login_btn.Destroy()
        print type(userinfo['username'])
        self.username = wx.StaticText(self, -1, unicode(userinfo['username']))
        self.name = wx.StaticText(self, -1, unicode(userinfo['name']))
        self.btn = wx.Button(self, -1, u'切换账号')
        self.Bind(wx.EVT_BUTTON, self.change_user, self.btn)
        self.sizer.AddMany([(self.name, 0, wx.EXPAND | wx.ALL, 10),
                            (self.username, 0, wx.EXPAND | wx.ALL, 10),
                            (wx.StaticText(self, -1, unicode(userinfo['class'])), 0,
                             wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 10),
                            (self.btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)])
        self.SetSize(self.GetBestSize())
        self.SetAutoLayout(True)
        self.sizer.Layout()
        self.Refresh()
        course = User.GetResult()[0] 
        SelectedPanel = wx.FindWindowByName('SelectedPanel')
        SelectedPanel.Update(course)
        SelectPanel = wx.FindWindowByName('SelectPanel')
        SelectPanel.InitCbsList()


    def change_user(self, event):
        global User
        dlg = LoginDialog(None, -1, u'请登录')
        dlg.CenterOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            User = dlg.GetUser()
            self.change('n')
            dlg.Destroy()


class WantPanel(wx.Panel):

    """已选的可以退选，从筛选区选择的"""

    def __init__(self, parent, label, btnlabel,name):
        super(WantPanel, self).__init__(parent,name=name)
        self.sbox = wx.StaticBox(self, -1, label=label)
        sboxsizer = wx.StaticBoxSizer(self.sbox, wx.HORIZONTAL)
        self.course_name = wx.StaticText(self,-1,u'')        
        self.name = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.day = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.time = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.place = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.campus = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.capacity = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.selectedman = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.able = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.sex_limit = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)        
        sboxsizer.AddMany([
            (self.course_name, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.day, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.time, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.place, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.campus, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.selectedman, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.capacity, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.sex_limit, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.able, 0, wx.ALIGN_CENTER | wx.RIGHT, 60)])
                
        self.btn = wx.Button(self, -1, btnlabel)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn)
        self.btn.Disable()
        sboxsizer.Add(self.btn, 0, wx.ALIGN_CENTER_VERTICAL)
        msizer = wx.BoxSizer(wx.HORIZONTAL)
        msizer.Add(sboxsizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(msizer)
    def Update(self,course):
        global User
        # if 
        self.course_id = course['course_id']
        self.course_name.SetLabel(course['course_name'])
        self.name.SetLabel(course['name'])      
        self.day.SetLabel(course['day'])        
        self.time.SetLabel(course['time'])       
        self.place.SetLabel(course['place'])      
        self.campus.SetLabel(course['campus'])
        self.btn.Enable()

        self.capacity.SetLabel(course['capacity'])   
        self.selectedman.SetLabel(course['selectedman'])
        self.able.SetLabel(course['able'])       
        self.sex_limit.SetLabel(course['sex_limit'])  
        
    def OnButton(self, event):
        global User
        btn = event.GetEventObject()
        if btn.GetLabel() == u'退选':
            User.SelectCourse('quit', self.course_id)
            print '退选'
        elif btn.GetLabel() == u"开抢":
            User.SelectCourse('select', self.course_id)
            print '开抢'
        else:
            print "Error"
class SelectedPanel(wx.Panel):

    """已选的可以退选，从筛选区选择的"""

    def __init__(self, parent, label, btnlabel,name):
        super(SelectedPanel, self).__init__(parent,name=name)
        self.sbox = wx.StaticBox(self, -1, label=label)
        sboxsizer = wx.StaticBoxSizer(self.sbox, wx.HORIZONTAL)
        self.course_name = wx.StaticText(self,-1,u'')        
        self.name = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.day = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.time = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.place = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.campus = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
        self.phone = wx.StaticText(self,-1,u'',(-1,-1),(-1,-1),wx.ALIGN_CENTER)
    
        sboxsizer.AddMany([
            (self.course_name, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.name, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.day, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.time, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.place, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.campus, 0, wx.ALIGN_CENTER | wx.RIGHT, 60),
            (self.phone, 0, wx.ALIGN_CENTER | wx.RIGHT, 60)])
                
        self.btn = wx.Button(self, -1, btnlabel)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn)
        self.btn.Disable()
        sboxsizer.Add(self.btn, 0, wx.ALIGN_CENTER_VERTICAL)
        msizer = wx.BoxSizer(wx.HORIZONTAL)
        msizer.Add(sboxsizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(msizer)
    def Update(self,course):
        global User
        # if 
        self.course_id = course['course_id']
        self.course_name.SetLabel(course['course_name'])
        self.name.SetLabel(course['name'])      
        self.day.SetLabel(course['day'])        
        self.time.SetLabel(course['time'])       
        self.place.SetLabel(course['place'])      
        self.campus.SetLabel(course['campus'])
        self.phone.SetLabel(course['phone'])

        self.btn.Enable()    
        
    def OnButton(self, event):
        global User
        btn = event.GetEventObject()
        if btn.GetLabel() == u'退选':
            User.SelectCourse('quit', self.course_id)
            print '退选'
        elif btn.GetLabel() == u"开抢":
            User.SelectCourse('select', self.course_id)
            print '开抢'
        else:
            print "Error"


class SelectPanel(wx.Panel):

    """docstring for SelectPanel"""

    def __init__(self, parent,name):
        super(SelectPanel, self).__init__(parent,name=name)
        # course_name name selectedman capacity campus place time day
        self.namemap = {1: {'name':'course_name','display':u'类型'},
                        2: {'name':'name','display':u'老师'},
                        3: {'name':'time','display':u'时间'},
                        4: {'name':'day','display':u'周几'},
                        5: {'name':'campus','display':u'校区'},
                        6: {'name':'place','display':u'地点'},
                        7: {'name':'capacity','display':u'容量'},
                        8: {'name':'selectedman','display':u'已选'},
                        9: {'name':'able','display':u'可选'},
                        0: {'name':'sex_limit','display':u'性别'}}
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CBs()
        self.vsizer.Add(self.hsizer, 0, wx.ALL, 10)
        self.CourseList()

        self.SetSizer(self.vsizer)

    def CBs(self):
        for index in range(len(self.namemap)):
            CB = wx.ComboBox(self,
                             -1,
                             self.namemap[index]['display'],
                             name=self.namemap[index]['name'],
                             size=(80, 25),
                             choices=[],
                             style=wx.CB_DROPDOWN | wx.CB_SORT)
            self.hsizer.Add(CB, 0, wx.RIGHT, 10)
            self.Bind(wx.EVT_COMBOBOX, self.OnCBs, CB)

    def CourseList(self):
        list_size = ((80 + 10) * len(self.namemap), -1)
        style = wx.LC_REPORT | wx.LC_SINGLE_SEL
        self.list = wx.ListCtrl(
            self, style=style, size=list_size, name='CourseList')
        for index in range(len(self.namemap)):
            self.list.InsertColumn(index, self.namemap[index]['display'])
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelect, self.list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.list)
        self.vsizer.Add(self.list, 0, wx.ALL, 10)

    def InitCbsList(self):
        global User
        self.ableCourse = User.GetAbleCourse()
        self.allCourse = User.GetAllCourse()
        self.AbleId = set()
        self.NotId = set()
        if self.ableCourse == 0:
            # 非选课时间
            pass
        elif self.ableCourse == -1:
            # 检索内容为空
            pass
        else:
            for course in self.ableCourse:
                course['able'] = '1'
                self.AbleId.add(course['course_id'])
        if self.allCourse != []:
            for course in self.allCourse:
                if course['course_id'] not in self.AbleId:
                    self.NotId.add(course['course_id'])
                    course['able'] = '0'
        # 为ComboBox整理数据 
        cbsdata = {'course_id': set(),
                   'course_name': set(),
                   'name': set(),
                   'selectedman': set(),
                   'capacity': set(),
                   'campus': set(),
                   'place': set(),
                   'time': set(),
                   'day': set(),
                   'sex_limit': set()}
        for course in self.allCourse:
            for k, v in course.iteritems():
                if k != 'able':
                    cbsdata[k].add(v)
        # 添加Cba的选项
        for field,data in cbsdata.iteritems():
            if field != 'course_id':
                cb = wx.FindWindowByName(field)
                cb.AppendItems(list(data))
        cb = wx.FindWindowByName('able')
        cb.AppendItems([u'全校',u'应选'])
        # 课程总数
        courseCount = len(self.AbleId) + len(self.NotId)
        # 添加所有课程需要的行
        for num in range(courseCount):
            self.list.InsertStringItem(num,'')
        # 添加应选课程
        if self.ableCourse == list:
            for course,row in map(None,self.ableCourse,range(len(self.AbleId))):
                for col in range(len(self.namemap)):
                    name = self.namemap[col]['name']
                    self.list.SetStringItem(row,col,coures[name])
                self.list.SetItemData(row,int(course['course_id']))
        # 添加不应选课程
        if type(self.allCourse) == list and self.allCourse != []:
            for course,row in map(None,self.allCourse,range(len(self.AbleId),len(self.NotId))):
                if course['able'] == '0':  
                    for col in range(len(self.namemap)):
                        name = self.namemap[col]['name']
                        self.list.SetStringItem(row,col,course[name])
                    self.list.SetItemData(row,int(course['course_id']))
    def OnCBs(self, event):
        cb = event.GetEventObject()
        choices = {'course_id': '',
                   'course_name': '', 
                   'name': '', 
                   'selectedman': '', 
                   'capacity': '', 
                   'campus': '', 
                   'place': '', 
                   'time': '', 
                   'day': '',
                   'sex_limit': '',
                   'able': ''}
        # 筛选数据
        wantAble = []
        wantNot = []
        for n in range(len(self.namemap)):
            name = self.namemap[n]['name']
            cb = wx.FindWindowByName(name)
            choices[name] = cb.GetStringSeleection()
        for course in self.allCourse:
            same = True
            for k,v in choices.iteritems():
                if v:
                    if course[k] != v:
                        same = False
                        break
            if same:
                if course['course_id'] in self.AbleId: 
                    wantAble.append(course)
                else:
                    wantNot.append(course)
        # 显示在ListCtrl上
        # 清除原来显示的
        self.list.DeleteAllItems()
        for row in range(len(wantNot)+len(wantAble)):
            self.list.InsertStringItem(row,'')
        for course,row in map(None,wantAble,range(len(wantAble))):
            for col in range(len(self.namemap)):
                name = self.namemap[col]['name']
                self.list.SetStringItem(row,col,course[name])
            self.list.SetItemData(row,int(course['course_id']))
        for course,row in map(None,wantNot,range(len(wantNot))):
            for col in range(len(self.namemap)):
                name = self.namemap[col]['name']
                self.list.SetStringItem(row,col,course[name])
            self.list.SetItemData(row,int(course['course_id']))
        # for index in range(cb.Count):
        # cb.Delete(index)
        # self.list.ClearAll() #ClearAll()会清除第一行
        # DeleteAllItems
        # SetItem
        # SetItemData
        # course_id course_name name selectedman capacity campus place time day sex_limit
        # pass

    def OnSelect(self, event):
        # cb.Delete(0) cb.Count
        # cb.Append("foo", "This is some client data for this item")
        # data = cb.GetClientData(evt.GetSelection())
        # evt.GetString()
        row = event.GetIndex()
        # courseId = item.GetData()
        course = {}
        for col in range(len(self.namemap)):
            key = self.namemap[col]['name']
            course[key] = self.list.GetItem(row,col).GetText()
        course['course_id'] = event.GetData()
        wantPanel = wx.FindWindowByName('WantPanel')
        wantPanel.Update(course)

class MainPanel(wx.Panel):

    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)
        self.SetAutoLayout(True)
        # 登陆模块
        self.userinfo = InfoPanel(self)
        self.selected = SelectedPanel(self, u'已选', u'退选','SelectedPanel')
        self.wanted = WantPanel(self, u'我选', u'开抢','WantPanel')
        self.select = SelectPanel(self,'SelectPanel')
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddMany([(self.userinfo, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 10),
                        (self.selected, 0, wx.ALIGN_CENTER_VERTICAL |
                         wx.EXPAND | wx.TOP, 5),
                        (self.wanted, 0, wx.ALIGN_CENTER_VERTICAL |
                         wx.EXPAND | wx.TOP, 5),
                        (self.select, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.TOP, 5)])

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
        menu.Append(wx.NewId(), u"作者", u'联系我哦')
        menuBar.Append(menu, u"联系我哦")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(),u'ok')
        menuBar.Append(menu2, u"帮我一把")

        menu3 = wx.Menu()
        menu3.Append(wx.NewId(),u'ok')
        menuBar.Append(menu3, u"商业赞助")

        menu4 = wx.Menu()
        menu4.Append(wx.NewId(),u'ok')
        menuBar.Append(menu4, u"有意见")
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

        wx.lib.inspection.InspectionTool().Show()
        self.frame.Show()

        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
