# _*_ coding:utf-8 _*_
#!/usr/bin/env python

#############
#  对话框   #
#############
import wx


class LoginDialog(wx.Dialog):

    def __init__(self, parent, id, title,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize):

        super(LoginDialog, self).__init__(parent, id, title, pos, size)
        self.panel = wx.Panel(self)
        # Sizer
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.username = wx.TextCtrl(self.panel, -1, name="username")
        name = wx.StaticText(self.panel, -1, u'学号')
        hsizer1.AddMany(((name, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 5),
                         (self.username, 0, wx.ALL, 5)
                         ))

        password = wx.TextCtrl(
            self.panel, -1, style=wx.TE_PASSWORD, name="password")
        passname = wx.StaticText(self.panel, -1, u'密码')
        hsizer2.AddMany(((passname, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 5),
                         (password, 0, wx.ALL, 5)
                         ))

        button = wx.Button(self.panel,1,u"登录")
        button.SetDefault()
        vsizer.AddMany(((hsizer1, 0, wx.ALL, 5),
                        (hsizer2, 0, wx.ALL, 5),
                        (button, 0, wx.ALL, 5)))
        self.panel.SetSizer(vsizer)

# class LoginPanel(wx.Panel):

    # def __init__(self,)
class TestFrame(wx.Frame):

    def __init__(self):
        super(TestFrame, self).__init__(None, -1, 'Test Frame')
        panel = wx.Panel(self)
        dlg = LoginDialog(None, wx.ID_OK, u'请登录')
        dlg.ShowModal()
        print dlg.username.GetValue()
        # if dlg.ShowModal() == wx.ID_OK:
            # dlg.Destory()
            # print 1

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestFrame()
    frame.Show()
    app.MainLoop()
