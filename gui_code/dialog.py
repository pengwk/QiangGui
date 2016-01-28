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
