# _*_ coding:utf-8 _*_
import os

import wx
import wx.lib.inspection

img_dir = "C:\\Users\\wk\\OneDrive\\W\\QiangGui\\img"

class SelectPanel(wx.Toolbook):
    """docstring for ClassName"""

    def __init__(self, parent, id):
        super(SelectPanel, self).__init__(parent, id, style=wx.BK_BOTTOM)

        # ImageList
        imagelist = wx.ImageList(75, 75)
        index_1 = imagelist.Add(wx.Image(os.path.join(img_dir, u"足球.jpg")).ConvertToBitmap())
        index_2 = imagelist.Add(wx.Image(os.path.join(img_dir, u"篮球.jpg")).ConvertToBitmap())
        index_3 = imagelist.Add(wx.Image(os.path.join(img_dir, u"瑜伽.jpg")).ConvertToBitmap())
        
        self.AssignImageList(imagelist)
        # 时间
        panel = TimePanel(self, wx.ID_ANY, None)
        self.AddPage(panel, u"时间", imageId=index_1)
        
        # 课程
        panel = CoursePanel(self, wx.ID_ANY, None)
        self.AddPage(panel, u"项目", imageId=index_2)

        # 老师
        panel = TeacherPanel(self, wx.ID_ANY, None)
        self.AddPage(panel, u"老师", imageId=index_3)

        # 间隔
        

        # 事件绑定
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        pass

    def OnPageChanging(self, event):
        pass

class TimePanel(wx.Panel):
    u"""时间选择
    """
    def __init__(self, parent, id, style):
        super(TimePanel, self).__init__(parent, id, style)

class CoursePanel(wx.Panel):
    u"""课程选择
    """
    def __init__(self, parent, id, style):
        super(CoursePanel, self).__init__(parent, id, style)

class TeacherPanel(wx.Panel):
    u"""老师选择
    """
    def __init__(self, parent, id, style):
        super(TeacherPanel, self).__init__(parent, id, style)

class MyFrame(wx.Frame):
    """"""

    def __init__(self, parent, id=wx.ID_ANY, title=u"MyFrame", name="MyFrame", pos=wx.DefaultPosition, size=(1000, 1000), style=wx.DEFAULT_FRAME_STYLE):
        super(MyFrame, self).__init__(parent, id, title, pos, size, style, name)

        # 居中
        self.Center()

        # 组件
        self.panel = SelectPanel(self, -1)
        
        # 布局
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(vsizer)

class MyApp(wx.App):

    def OnInit(self):

        self.frame = MyFrame(None, title=u"抢课")
        size = self.frame.GetBestSize()
        self.frame.SetSize(size)
        self.SetTopWindow(self.frame)
        wx.lib.inspection.InspectionTool().Show()
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(None)
    app.MainLoop()
