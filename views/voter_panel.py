import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import controllers.worksheet_controller as controller
from views.turonout_menu import TurnoutMenu
from controllers.voter_controller import VoterController


class VoterPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(-1, 500))
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_tb_panel(self)
        layout.Add(tb, 0, wx.EXPAND, 5)

        lst_panel = self.build_lst_panel(self)
        layout.Add(lst_panel, 0, wx.EXPAND, 5)

        self.SetSizer(layout)

        self.addr_sort_asc = True

        # self.turnout_menu = TurnoutMenu(self)
        #
        # self.controller = VoterController(self)

    def build_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Voters')
        layout.Add(lbl, 0, wx.ALL | wx.EXPAND, 5)

        self.select_btn = uil.toolbar_button(panel, 'Make Selection')
        layout.Add(self.select_btn, 0, wx.ALL, 5)

        self.save_btn = uil.toolbar_button(panel, 'Save This List')
        layout.Add(self.save_btn, 0, wx.ALL, 5)

        self.open_btn = uil.toolbar_button(panel, 'Load Saved List')
        layout.Add(self.open_btn, 0, wx.ALL, 5)

        self.print_btn = uil.toolbar_button(panel, 'Print This List')
        layout.Add(self.print_btn, 0, wx.ALL, 5)

        self.deselect_btn = uil.toolbar_button(panel, 'Show All')
        layout.Add(self.deselect_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

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
            olv.ColumnDefn('Name', 'left', valueGetter=str),
            olv.ColumnDefn('Address', 'left', valueGetter='street_address'),
            olv.ColumnDefn('Gender', 'left', valueGetter='gender'),
            olv.ColumnDefn('Age Group', 'left', valueGetter='age_group'),
            # olv.ColumnDefn('Party', 'left', valueGetter='party'),
            olv.ColumnDefn('Score', 'left', valueGetter='score')
        ]
        self.voter_list_ctrl.SetColumns(self.voter_list_cols)
        self.add_election_cols()
        self.voter_list_ctrl.SetSortColumn(0)
        self.voter_list_ctrl.AutoSizeColumns()
        self.voter_list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.list_sorter_evt)
        layout.Add(self.voter_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def list_sorter_evt(self, evt):
        if evt.Column == 1:
            self.voter_list_ctrl.SortListItemsBy(self.list_sorter)
            self.addr_sort_asc = not self.addr_sort_asc
        else:
            evt.Skip()

    def list_sorter(self, obj1, obj2):
        return obj1.addr_cmp(obj2, self.addr_sort_asc)

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
        self.voter_list_ctrl.SortBy(0)

    def get_list(self):
        return self.voter_list_ctrl.GetObjects()

    def load_my_list(self, objs):
        self.voter_list_ctrl.SetObjects(objs)
