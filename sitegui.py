import wx
import pulldata as pd

import wx
import wx.lib.agw.hyperlink


class HomePage(wx.Frame):
    def __init__(self, parent, title):
        super(HomePage, self).__init__(parent, title=title, size=(600, 200))
        self.large_border = 10
        self.med_border = 7
        self.small_border = 5
        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        url_lbl = wx.StaticText(panel, label='url:')
        url_input = wx.TextCtrl(panel, value='', style=wx.TE_AUTO_URL)
        url_input.SetValue("http://")
        hbox0.Add(url_lbl, flag=wx.ALL, border=self.small_border)
        hbox0.Add(url_input, proportion=1)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        num_lvls_lbl = wx.StaticText(panel, label='Map Depth:')
        num_lvls_input = wx.TextCtrl(panel, value='')
        hbox1.Add(num_lvls_lbl, flag=wx.ALL, border=self.small_border)
        hbox1.Add(num_lvls_input)

        vbox.Add(hbox0, flag=wx.EXPAND | wx.ALL, border=self.small_border)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=self.small_border)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Map Site', size=(70, 30))
        
        btn2 = wx.Button(panel, label='Cancel', size=(70, 30))
        hbox2.Add(btn1, flag=wx.ALL, border=self.small_border)
        hbox2.Add(btn2, flag=wx.ALL, border=self.small_border)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        cb0 = wx.CheckBox(panel, label="Ignore add sub-layers")
        cb0.SetValue(True)
        cb1 = wx.CheckBox(panel, label="Ignore social media sub-layers")
        cb1.SetValue(True)
        cb2 = wx.CheckBox(panel, label="Ignore wiki sub-layers")
        cb2.SetValue(True)
        hbox3.Add(cb0, flag=wx.ALL, border=self.small_border)
        hbox3.Add(cb1, flag=wx.ALL, border=self.small_border)
        hbox3.Add(cb2, flag=wx.ALL, border=self.small_border)

        vbox.Add(hbox3)

        vbox.Add(hbox2, flag=wx.ALL, border=self.small_border)

        panel.SetSizer(vbox)


class SettingsWindow(wx.Frame):
    def __init__(self, parent, title):
        super(SettingsWindow, self).__init__(parent, title, size=(600, 800))


if __name__ == '__main__':
    app = wx.App()
    HomePage(None, title='SiteMap')
    app.MainLoop()
