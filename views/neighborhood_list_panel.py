import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from controllers.neighborhood_controller import NeighborhoodController


class NeighborhoodPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lst_panel = self.build_lst_panel(self)
        layout.Add(lst_panel, 0, wx.EXPAND, 5)

        frm_panel = self.build_frm_panel(self)
        layout.Add(frm_panel, 0, wx.EXPAND, 5)

        grf = self.build_grf_panel(self)
        layout.Add(grf, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(layout)

        self.controller = NeighborhoodController(self)

    def build_lst_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition,
                         size=(-1, -1))
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_lst_tb_panel(panel)
        layout.Add(tb, 0, wx.EXPAND | wx.ALL, 5)

        lst = self.build_lst_lst_panel(panel)
        layout.Add(lst, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_lst_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Neighborhoods')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.new_nhood_btn = uil.toolbar_button(panel, 'New Neighborhood')
        layout.Add(self.new_nhood_btn, 0, wx.ALL, 5)

        self.drop_nhood_btn = uil.toolbar_button(panel, 'Drop Neighborhood')
        layout.Add(self.drop_nhood_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_lst_lst_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.nhood_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                  size=(-1, -1),
                                                  style=flags)
        self.nhood_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.nhood_list_ctrl.SetColumns([
            olv.ColumnDefn('My Neighborhoods', 'left', 300, 'name'),
        ])
        layout.Add(self.nhood_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel

    def load_neighborhoods(self, nhoods):
        self.nhood_list_ctrl.SetObjects(nhoods)

    def select_neighborhood(self, idx):
        self.nhood_list_ctrl.Select(idx)

    def build_frm_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_frm_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        frm_panel = self.build_frm_frm_panel(panel)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

        return panel

    def build_frm_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Streets')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.new_street_btn = uil.toolbar_button(panel, 'Add Street')
        layout.Add(self.new_street_btn, 0, wx.ALL, 5)

        self.drop_street_btn = uil.toolbar_button(panel, 'Drop Street')
        layout.Add(self.drop_street_btn, 0, wx.ALL, 5)

        self.save_street_btn = uil.toolbar_button(panel, 'Save Edits')
        layout.Add(self.save_street_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_frm_frm_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.street_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                   size=(-1, -1),
                                                   style=flags)
        self.street_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.street_list_ctrl.SetColumns([
            olv.ColumnDefn('Street', 'left', 250, 'name'),
            olv.ColumnDefn('From', 'left', 50, 'lo'),
            olv.ColumnDefn('To', 'left', 50, 'hi'),
            olv.ColumnDefn('Side', 'left', 50, 'oe'),
        ])
        layout.Add(self.street_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def load_streets(self, data):
        self.street_list_ctrl.SetObjects(data)

    def build_grf_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_grf_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        lst_panel = self.build_grf_list_panel(panel)
        layout.Add(lst_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

        return panel

    def build_grf_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Turnout Graphs')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.show_grf_btn = uil.toolbar_button(panel, 'Show Graph')
        layout.Add(self.show_grf_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_grf_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        self.grf_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                size=(-1, -1),
                                                style=flags)
        self.grf_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.grf_list_ctrl.SetColumns([
            olv.ColumnDefn('Graph', 'left', 250, 'name'),
        ])
        layout.Add(self.grf_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel

    def load_grf_list(self, items):
        self.grf_list_ctrl.SetObjects(items)

    def get_grf_selections(self):
        return self.grf_list_ctrl.GetSelectedObjects()

    def get_current_nhood(self):
        return self.nhood_list_ctrl.GetSelectedObject().name
