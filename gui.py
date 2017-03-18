#!python
import wx
import webbrowser


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700, 500))
        self.CreateStatusBar()
        menu_file = wx.Menu()

        menu_file_about = menu_file.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.on_about, menu_file_about)

        menu_file.AppendSeparator()

        menu_file_exit = menu_file.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.on_exit, menu_file_exit)

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_file, "&File")
        self.SetMenuBar(menu_bar)

        self.Show(True)

    def on_about(self, e):
        webbrowser.open('https://github.com/Himura2la/Cosplay2-Downloader')
        # dlg = wx.MessageDialog(self, "Check your browser, bro.",
        #                         "About " + self.Label, wx.OK)
        # dlg.ShowModal()
        # dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainFrame(None, 'Cosplay2 Downloader')
app.MainLoop()