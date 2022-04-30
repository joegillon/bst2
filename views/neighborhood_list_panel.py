import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
# from controllers.neighborhood_controller import NeighborhoodController


class NeighborhoodListPanel(wx.Panel):

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

    def load_neighborhoods(self, nhoods):
        self.nhood_list_ctrl.SetObjects(nhoods)

    def select_neighborhood(self, idx):
        self.nhood_list_ctrl.Select(idx)

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

   def build_nhoods_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Create Neighborhoods')
        layout.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_nhoods_frm_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['frmBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        lbl_layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl_street = uil.toolbar_label(panel, 'Street')
        lbl_layout.Add(lbl_street, 0, wx.ALL, 5)

        lbl_from = uil.toolbar_label(panel, 'From')
        lbl_layout.Add(lbl_from, 0, wx.ALL, 5)

        lbl_to = uil.toolbar_label(panel, 'To')
        lbl_layout.Add(lbl_to, 0, wx.ALL, 5)

        lbl_side = uil.toolbar_label(panel, 'Side')
        lbl_layout.Add(lbl_side, 0, wx.ALL, 5)

        layout.Add(lbl_layout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel
