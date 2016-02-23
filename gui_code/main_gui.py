# _*_ coding:utf-8 _*_

import wx
import wx.grid as Grid
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
        # print "I need change panel for user"
        # print button_name
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

        time_select_panel = TimeSelectPanel(self, u"time_select_panel")
        course_select_panel = CourseSelectPanel(self, u"course_select_panel")
        teacher_select_panel = TeacherSelectPanel(
            self, u"teacher_select_panel")

        self.vsizer.AddMany([(time_select_panel, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),
                             (course_select_panel, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),
                             (teacher_select_panel, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),])


        wx.FindWindowByName(u"course_select_panel").Hide()
        wx.FindWindowByName(u"teacher_select_panel").Hide()

        self.SetSizer(self.vsizer)

    def change_content(self, panel_name):
        widget_names = [u"course_select_panel",
                        u"time_select_panel", u"teacher_select_panel"]
        for widget_name in widget_names:
            if widget_name == panel_name:
                wx.FindWindowByName(widget_name).Show()
                self.GetParent().Layout()
            else:
                self.vsizer.Hide(wx.FindWindowByName(widget_name))

                # wx.FindWindowByName(widget_name).Hide()
                # self.vsizer.Layout()
                self.GetParent().Layout()


class FilterPanel(wx.Panel):

    def __init__(self, parent):
        super(FilterPanel, self).__init__(parent, size=(900, 200))


# 具体选择的面板

class TimeSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TimeSelectPanel, self).__init__(
            parent, name=name, )
        # bug
        self.counter = 0
        # self.SetBackgroundColour("red")

        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_grid = Grid.Grid(self, name="time_grid")
        self.time_grid.EnableEditing(False) # 禁止编辑
        self.time_grid.DisableDragGridSize() # 禁止在网格区缩放表格
        self.time_grid.DisableDragRowSize()  # 禁止在行标题区拉伸表格
        self.time_grid.DisableDragColSize()  # 禁止在列标题区拉伸网格
        self.time_grid.SetSelectionBackground((255, 255, 255)) # 选择前景色为白色 看不见拖拽选择
        self.time_grid.SetCellHighlightPenWidth(0) # 去掉单击高亮时显示的框
        
        self.time_grid.Bind(Grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelClick)
        self.time_grid.Bind(Grid.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.time_grid.Bind(Grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        
        self.time_grid.CreateGrid(5, 8)
        

        # 显示星期几 
        for row, num_cn in enumerate([u"一", u"二", u"三", u"四", u"五"]):
            self.time_grid.SetRowLabelValue(row, u"星期{}".format(num_cn))
        # 显示第几节
        for col, num_cn in enumerate([u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八"]):
            self.time_grid.SetColLabelValue(col, u"第{}节".format(num_cn))

        self.vsizer.Add(self.time_grid, 2, wx.EXPAND)
        self.SetSizer(self.vsizer)

    def OnLabelClick(self, event):
        u"""阻止用户点击标签栏，选择整行或整列"""
        event.Veto()

    def OnRangeSelect(self, event):
        u"""看不见鼠标拖动选择"""
        if self.time_grid.GetSelectionBlockTopLeft() ==  self.time_grid.GetSelectionBlockBottomRight():
            pass
        else:
            self.time_grid.ClearSelection()
            self.counter = self.counter + 1 
            print "clear selection{}".format(self.counter)
    
    def OnCellLeftClick(self, event):
        u""""""
        print "CellClick"

        row = event.GetRow()
        col = event.GetCol()

        selected_color = wx.Colour(255, 0, 0)
        white = wx.Colour(255, 255, 255)
        old_color = self.time_grid.GetCellBackgroundColour(row, col)
        # 取消选择
        if old_color == selected_color: # 红色
            self.time_grid.SetCellBackgroundColour(row, col, white)
        else:
            self.time_grid.SetCellBackgroundColour(row, col, selected_color)
        self.time_grid.Refresh()

class CourseSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(CourseSelectPanel, self).__init__(
            parent, name=name)
        # bug
        self.SetBackgroundColour("blue")

        content = wx.StaticText(self, label=u"课程选择面板")
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(content, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.vsizer)


class TeacherSelectPanel(wx.Panel):
    u""""""

    def __init__(self, parent, name):
        super(TeacherSelectPanel, self).__init__(
            parent, name=name)
        # bug
        self.SetBackgroundColour("gray")

        content = wx.StaticText(self, label=u"老师选择面板",
                                style=wx.ALIGN_CENTER_HORIZONTAL)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(content, 1, wx.EXPAND | wx.ALL, 5)
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
        # 修复时间选择启动不显示
        self.frame.Layout()
        return True

if __name__ == "__main__":
    app = MyApp(redirect=False, useBestVisual=True)
    app.MainLoop()
