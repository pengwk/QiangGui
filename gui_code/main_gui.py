# _*_ coding:utf-8 _*_

import wx
import wx.grid
import wx.lib.inspection

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
        hsizer.AddMany(((time_button, 1, wx.ALL, 10,),
                        (class_button, 1, wx.ALL, 10,),
                        (teacher_button, 1, wx.ALL, 10,)))

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
            self.ChangePanel(button_name)

    def ChangePanel(self, button_name):
        #print "I need change panel for user"
        #print button_name
        button_to_panel = {u"course_button": u"course_select_panel",  # course_select_panel
                           u"teacher_button": u"teacher_select_panel",
                           u"time_button": u"time_select_panel"}

        panel = wx.FindWindowByName(u"select_panel")
        panel.change_content(button_to_panel[button_name])


class SelectPanel(wx.Panel):
    u"""不显示具体内容
    """

    def __init__(self, parent, name):
        super(SelectPanel, self).__init__(
            parent, size=(900, 400), name=name)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        
        self.vsizer.Add(TimeSelectPanel(self, u"time_select_panel"), 1, wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.vsizer.Add(CourseSelectPanel(self, u"course_select_panel"), 1, wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.vsizer.Add(TeacherSelectPanel(self, u"teacher_select_panel"), 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

        wx.FindWindowByName(u"course_select_panel").Hide()
        wx.FindWindowByName(u"teacher_select_panel").Hide()

        self.SetSizer(self.vsizer)


    def change_content(self, panel_name):
        widget_names = [u"course_select_panel", u"time_select_panel", u"teacher_select_panel"]
        for widget_name in widget_names:
            if widget_name == panel_name:
                wx.FindWindowByName(widget_name).Show()
                self.GetParent().Layout()
            else:
                self.vsizer.Hide(wx.FindWindowByName(widget_name))
               
                #wx.FindWindowByName(widget_name).Hide()
                #self.vsizer.Layout()
                self.GetParent().Layout()


class FilterPanel(wx.Panel):

    def __init__(self, parent):
        super(FilterPanel, self).__init__(parent, size=(900, 200))


# 具体选择的面板

class TimeSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TimeSelectPanel, self).__init__(
            parent, name=name, size=(900, 400))
        # bug 
        #self.SetBackgroundColour("red")
        
        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        time_grid = wx.grid.Grid(self)
        time_grid.CreateGrid(5,10)
        time_grid.SetCellValue(0, 0, "First cell")

        
        #content = wx.StaticText(self, label=u"时间选择面板")
        self.vsizer.Add(time_grid, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.vsizer)
        

class CourseSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(CourseSelectPanel, self).__init__(
            parent, name=name)
        # bug
        self.SetBackgroundColour("blue")

        content = wx.StaticText(self, label=u"课程选择面板")
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(content, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.vsizer)
        

class TeacherSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TeacherSelectPanel, self).__init__(
            parent, name=name)
        # bug 
        self.SetBackgroundColour("gray")

        content = wx.StaticText(self, label=u"老师选择面板", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(content, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.vsizer)
        

class MyFrame(wx.Frame):

    def __init__(self, parent, id, title, pos, size, style, name):
        super(MyFrame, self).__init__(
            parent, id, title, pos, size, style, name)
        #self.panel = wx.Panel(self)

        # 布局
        self._DoLayOut()

    def _DoLayOut(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vsizer)

        vsizer.AddMany(((FilterPanel(self), 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),
                        (SelectPanel(self, u"select_panel"), 1, wx.ALL |
                         wx.ALIGN_CENTER_HORIZONTAL, 5),
                        (ButtonPanel(self), 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),))


class MyApp(wx.App):

    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, u"抢课", wx.DefaultPosition,
                             (1000, 750), wx.DEFAULT_FRAME_STYLE, MyFrameNAME)

        #size = self.frame.GetBestSize()
        # self.frame.SetSize(size)

        self.SetTopWindow(self.frame)

        # inspection 工具
        wx.lib.inspection.InspectionTool().Show()

        self.frame.Show()
        self.frame.Center()
        return True

if __name__ == "__main__":
    app = MyApp(redirect=False, useBestVisual=True)
    app.MainLoop()
