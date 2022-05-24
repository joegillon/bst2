import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import controllers.residence_controller as controller


class ResidencePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(-1, 500))
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_tb_panel(self)
        layout.Add(tb, 0, wx.EXPAND, 5)

        lst_panel = self.build_lst_panel(self)
        layout.Add(lst_panel, 0, wx.EXPAND, 5)

        self.SetSizer(layout)

        self.addr_sort_asc = False
        self.sort_fld = 0

    def build_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Residences')
        layout.Add(lbl, 0, wx.ALL | wx.EXPAND, 5)

        select_btn = uil.toolbar_button(panel, 'Make Selection')
        select_btn.Bind(wx.EVT_BUTTON, self.select_btn_click)
        layout.Add(select_btn, 0, wx.ALL, 5)

        save_btn = uil.toolbar_button(panel, 'Save This List')
        save_btn.Bind(wx.EVT_BUTTON, self.save_btn_click)
        layout.Add(save_btn, 0, wx.ALL, 5)

        open_btn = uil.toolbar_button(panel, 'Load Saved List')
        open_btn.Bind(wx.EVT_BUTTON, self.open_btn_click)
        layout.Add(open_btn, 0, wx.ALL, 5)

        print_btn = uil.toolbar_button(panel, 'Print This List')
        print_btn.Bind(wx.EVT_BUTTON, self.print_btn_click)
        layout.Add(print_btn, 0, wx.ALL, 5)

        deselect_btn = uil.toolbar_button(panel, 'Show All')
        deselect_btn.Bind(wx.EVT_BUTTON, self.deselect_btn_click)
        layout.Add(deselect_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def select_btn_click(self, evt):
        self.filter()

    def save_btn_click(self, evt):
        with wx.FileDialog(self, 'Save List',
                           wildcard='List files (*.csv)|*.csv',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dlg.GetPath()
            try:
                with open(pathname, 'w', newline='') as file:
                    controller.save_list(self.voter_list_ctrl.GetObjects(), file)
            except IOError:
                wx.MessageDialog(self, 'Unable to save to %s' % pathname).ShowModal()

    def open_btn_click(self, evt):
        with wx.FileDialog(self, 'Open Saved List',
                           wildcard='List files (*.csv)|*.csv',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dlg.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.voter_list_ctrl.SetObjects(controller.load_file(file))
            except IOError:
                wx.MessageDialog(self, 'Unable to open to %s' % pathname).ShowModal()

    def print_btn_click(self, evt):
        dlg = wx.MessageDialog(self, 'This will print the currently visible rows', 'Promises').ShowModal()

    def deselect_btn_click(self, evt):
        self.load_voters(controller.get_voters_by_residence())
        self.default_sort()

    def build_lst_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, size=(-1, 500))
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        self.voter_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                  size=(-1, 500),
                                                  style=flags)
        self.voter_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.voter_list_cols = [
            olv.ColumnDefn('Address', 'left', valueGetter='street_address'),
            olv.ColumnDefn('Name', 'left', valueGetter=str),
            olv.ColumnDefn('Gender', 'left', valueGetter='gender'),
            olv.ColumnDefn('Age Group', 'left', valueGetter='age_group'),
            olv.ColumnDefn('Score', 'left', valueGetter='score'),
        ]
        self.voter_list_ctrl.SetColumns(self.voter_list_cols)
        self.add_election_cols()
        self.voter_list_ctrl.AutoSizeColumns()
        self.voter_list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.list_sorter_evt)
        layout.Add(self.voter_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def list_sorter_evt(self, evt):
        if evt.Column == 0:
            self.default_sort()
        elif evt.Column == 1:
            evt.Skip()
        else:
            self.sort_fld = evt.EventObject.columns[evt.Column].valueGetter
            self.voter_list_ctrl.SortListItemsBy(self.list_non_addr_sorter)
        self.addr_sort_asc = not self.addr_sort_asc

    def list_addr_sorter(self, obj1, obj2):
        return obj1.addr_cmp(obj2, self.addr_sort_asc)

    def list_non_addr_sorter(self, obj1, obj2):
        return obj1.non_addr_cmp(self.sort_fld, obj2, self.addr_sort_asc)

    def load_voters(self, voters):
        self.voter_list_ctrl.SetObjects(voters)

    def add_election_cols(self):
        edates = [e.date for e in gbl.dataset.my_elections]
        for col in edates:
            self.voter_list_ctrl.AddColumnDefn(olv.ColumnDefn(col,
                                                              'right',
                                                              valueGetter=col,
                                                              fixedWidth=80))

    def filter(self):
        objs = self.voter_list_ctrl.GetSelectedObjects()
        self.voter_list_ctrl.SetObjects(objs)

    def default_sort(self):
        self.voter_list_ctrl.SortListItemsBy(self.list_addr_sorter)
