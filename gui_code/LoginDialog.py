# _*_ coding:utf-8 _*_
#!/usr/bin/env python


import wx
from login import Physcial

class LoginPanel(wx.Panel):

    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent)

        self._user = None
        self._username = wx.TextCtrl(self)
        self._password = wx.TextCtrl(self, style=wx.TE_PASSWORD)

        # Layout
        sizer = wx.FlexGridSizer(2, 2, 8, 8)
        sizer.AddMany(((wx.StaticText(self, label=u"学号"), 0, wx.ALIGN_CENTER_VERTICAL),
                       (self._username, 0, wx.EXPAND),
                       (wx.StaticText(self, label=u"密码"),
                        0, wx.ALIGN_CENTER_VERTICAL),
                       (self._password, 0, wx.EXPAND)))

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(sizer, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 20)

        # 登录按钮
        button = wx.Button(self, id=wx.ID_OK, label=u'登录')
        self.Bind(wx.EVT_BUTTON,self.login,button)
        button.SetDefault()

        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(button)

        mainsizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 12)
        # 按钮添加完成后 在不同平台上重新排列按钮
        btnsizer.Realize()
        self.SetSizer(mainsizer)

    def GetUsername(self):
        return self._username.GetValue()

    def GetPassword(self):
        return self._password.GetValue()
    def GetUser(self):
        return self._user
    def login(self,event):

        username = self._username.GetValue()
        password = self._password.GetValue()
        button = event.GetEventObject()
        button.SetLabel(u"正在登录")
        self._user = Physcial(username,password)
        try:
            self._user.Login()
            event.Skip()
        except ValueError:
            dialog = wx.FindWindowByName('LoginDialog')
            dialog.SetTitle(u'学号或密码错误')
            button.SetLabel(u'登录')
        


class LoginDialog(wx.Dialog):
# wx.SUNKEN_BORDER wx.DEFAULT_DIALOG_STYLE 
    def __init__(self, parent, id, title,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE,
                 name='LoginDialog'):
        super(LoginDialog, self).__init__(parent, id, title, pos, size, style,name)

        self.panel = LoginPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetInitialSize()
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        
    def OnClose(self,event):
        self.EndModal(-1)

    def GetUsername(self):
        return self.panel.GetUsername()

    def GetPassword(self):
        return self.panel.GetPassword()

    def GetUser(self):
        return self.panel.GetUser()


class TestFrame(wx.Frame):

    def __init__(self):
        super(TestFrame, self).__init__(None, -1, 'Test Frame')
        panel = wx.Panel(self)
        dlg = LoginDialog(None, -1, u'请登录')
        # 使对话框居中显示
        dlg.CenterOnParent()
        # dlg.CenterOnScreen()
        # dlg.ShowModal()
        # print dlg.GetUsername()
        if dlg.ShowModal() == wx.ID_OK:
            print dlg.GetUsername()
            print dlg.GetPassword()
        # dlg.Destory()
        # print 1

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestFrame()
    frame.Show()

    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()  
