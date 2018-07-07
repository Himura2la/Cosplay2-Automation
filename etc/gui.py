#!python
import wx
import wx.grid
import webbrowser


class MainFrame(wx.Frame):
    c2_info = None
    c2_info_filename = "c2_info.txt"
    grid_no_data_text = 'No data'
    grid_no_data_width = 100

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700, 500))

        # ------------------ Menu ------------------
        menu_bar = wx.MenuBar()  # TODO: use wx.ToolBar instead

        # --- File ---
        menu_file = wx.Menu()
        menu_file_about = menu_file.Append(wx.ID_ABOUT, "&About")
        self.Bind(wx.EVT_MENU, self.on_about, menu_file_about)
        menu_file_exit = menu_file.Append(wx.ID_EXIT, "E&xit")
        self.Bind(wx.EVT_MENU, self.on_exit, menu_file_exit)
        menu_bar.Append(menu_file, "&File")

        # --- Cosplay2 ---
        menu_c2 = wx.Menu()
        self.menu_c2_info = menu_c2.Append(wx.NewId(), "&Set login data",
                                       "Enter your Cosplay2 credentials...")
        self.Bind(wx.EVT_MENU, self.on_c2_info, self.menu_c2_info)
        menu_c2_login = menu_c2.Append(wx.NewId(), "&Log in!",
                                       "Log into your Cosplay2 account")
        self.read_c2_info()
        self.Bind(wx.EVT_MENU, self.on_c2_login, menu_c2_login)
        menu_bar.Append(menu_c2, "&Cosplay2")

        # --- Database ---
        menu_db = wx.Menu()
        menu_db_create = menu_db.Append(wx.NewId(), "Creat&e",
                                        "Create a new database...")
        self.Bind(wx.EVT_MENU, self.on_db_create, menu_db_create)
        menu_db_connect = menu_db.Append(wx.NewId(), "Co&nnect",
                                         "Connect to an existing database...")
        self.Bind(wx.EVT_MENU, self.on_db_connect, menu_db_connect)
        self.menu_db_query = menu_db.Append(wx.NewId(), "&Query",
                                       "Execute an SQL query...")
        self.menu_db_query.Enable(False)
        self.Bind(wx.EVT_MENU, self.on_db_query, self.menu_db_query)
        menu_bar.Append(menu_db, "&Database")

        self.SetMenuBar(menu_bar)

        # ------------------ Main Sizer ------------------
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Actions panel ---
        self.actions_panel = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.actions_panel, 0, wx.EXPAND)

        # --- Table ---
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(1, 1)
        self.grid.SetCellValue(0, 0, self.grid_no_data_text)
        self.grid.SetColSize(0, self.grid_no_data_width)
        self.grid_column_readonly(0)

        main_sizer.Add(self.grid, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

        # ------------------ Status Bar ------------------
        self.status_bar = self.CreateStatusBar(3)

        self.status("Ready")
        self.db_status("Disconnected")
        self.c2_status("Disconnected")

        self.Show(True)

    def status(self, text):
        self.status_bar.SetStatusText(text, 0)

    def on_about(self, e):
        webbrowser.open('https://github.com/Himura2la/Cosplay2-Downloader')
        # dlg = wx.MessageDialog(self, "Check your browser, bro.",
        #                         "About " + self.Label, wx.OK)
        # dlg.ShowModal()
        # dlg.Destroy()

    def on_exit(self, e):
        self.Close(True)

    def grid_set_shape(self, new_rows, new_cols, default_col_size=None):
        current_rows, current_cols = self.grid.GetNumberRows(), self.grid.GetNumberCols()
        if new_rows < current_rows:
            self.grid.DeleteRows(0, current_rows - new_rows, True)
        if new_cols < current_cols:
            self.grid.DeleteCols(0, current_cols - new_cols, True)
        if new_rows > current_rows:
            self.grid.AppendRows(new_rows - current_rows)
        if new_cols > current_cols:
            self.grid.AppendCols(new_cols - current_cols)

        if default_col_size:
            map(lambda col: self.grid.SetColSize(col, default_col_size), range(new_cols))

    def grid_column_readonly(self, col):
        grid_disabled_color = wx.Colour(240, 240, 240)

        def disable_cell(cell):
            self.grid.SetReadOnly(*cell)
            self.grid.SetCellBackgroundColour(*(cell + (grid_disabled_color,)))
        map(disable_cell, [(row, col) for row in range(self.grid.GetNumberRows())])

    # ------------------ Cosplay2 ------------------

    def c2_status(self, text):
        self.status_bar.SetStatusText("[C2] " + text, 2)

    def read_c2_info(self):
        try:
            self.c2_info = open(self.c2_info_filename).read().split()
        except IOError:
            return False
        return True

    def on_c2_info(self, e):
        self.menu_c2_info.Enable(False)
        self.grid.ClearGrid()
        self.grid_set_shape(2, 2, 100)
        self.grid.SetColSize(1, 200)
        self.grid.SetCellValue(0, 0, "Event Name")
        self.grid.SetCellValue(1, 0, "Org Login")
        self.grid_column_readonly(0)

        if not self.read_c2_info():
            self.c2_info = ["", ""]

        self.grid.SetCellValue(0, 1, self.c2_info[0])
        self.grid.SetCellValue(1, 1, self.c2_info[1])

        apply_button = wx.Button(self, wx.ID_APPLY)
        self.Bind(wx.EVT_BUTTON, self.on_c2_info_apply, apply_button)
        self.actions_panel.Add(apply_button, 1)
        self.Layout()

    def on_c2_info_apply(self, e):

        self.c2_info = self.grid.GetCellValue(0, 1), self.grid.GetCellValue(1, 1)

        if any(map(lambda x: len(x) < 3, self.c2_info)):
            self.status("Your data seems to be invalid...")
            return

        with open(self.c2_info_filename, 'w') as f:
            f.write(' '.join(self.c2_info))

        if not self.read_c2_info():
            self.status("Something went wrong T_T")
            return
        self.menu_c2_info.Enable(True)
        self.grid.ClearGrid()
        self.grid_set_shape(1, 1, self.grid_no_data_width)
        self.grid_column_readonly(0)
        self.grid.SetCellValue(0, 0, self.grid_no_data_text)
        self.actions_panel.Clear()
        self.Layout()
        self.status("Default credentials saved at " + self.c2_info_filename)

    def on_c2_login(self, e):
        pass

    # ------------------ Database ------------------

    def db_status(self, text):
        self.status_bar.SetStatusText("[DB] " + text, 1)

    def on_db_create(self, e):
        pass

    def on_db_connect(self, e):
        pass

    def on_db_query(self, e):
        pass

app = wx.App(False)
frame = MainFrame(None, 'Cosplay2 Downloader')
app.MainLoop()
