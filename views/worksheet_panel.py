import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from views.voter_panel import VoterPanel
from views.residence_panel import ResidencePanel
import controllers.worksheet_controller as controller


class WorksheetPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        top_layout = wx.BoxSizer(wx.HORIZONTAL)
        nhood_panel = self.build_nhood_panel(self)
        top_layout.Add(nhood_panel, 0, wx.ALL | wx.EXPAND, 5)

        turnout_graph_panel = self.build_turnout_graph_panel(self)
        top_layout.Add(turnout_graph_panel, 0, wx.ALL | wx.EXPAND, 5)

        makeup_graph_panel = self.build_makeup_graph_panel(self)
        top_layout.Add(makeup_graph_panel, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(top_layout, 0, wx.ALL | wx.EXPAND, 5)

        bottom_layout = wx.BoxSizer(wx.VERTICAL)

        self.voter_panel = VoterPanel(self)
        self.residence_panel = ResidencePanel(self)
        self.voter_panel.Hide()

        bottom_layout.Add(self.voter_panel, 1, wx.ALL | wx.EXPAND, 5)
        bottom_layout.Add(self.residence_panel, 1, wx.ALL | wx.EXPAND, 5)

        layout.Add(bottom_layout, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.nhood_list_ctrl.Select(0)

    def build_nhood_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_nhood_toolbar_panel(panel)
        lst = self.build_nhood_list_panel(panel)

        layout.Add(tb, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def build_nhood_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Neighborhoods')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.view_toggle = uil.toolbar_button(panel, 'By Residence')
        self.view_toggle.Bind(wx.EVT_BUTTON, self.on_view_toggle)
        layout.Add(self.view_toggle, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def on_view_toggle(self, evt):
        nhood = self.nhood_list_ctrl.GetSelectedObject()
        if self.voter_panel.IsShown():
            self.voter_panel.Hide()
            self.residence_panel.Show()
            self.residence_panel.voter_list_ctrl.Select(0)
            self.view_toggle.SetLabel('By Voter')
        else:
            self.residence_panel.Hide()
            self.voter_panel.Show()
            self.voter_panel.voter_list_ctrl.SetObjects(nhood.voters)
            self.voter_panel.voter_list_ctrl.Select(0)
            self.view_toggle.SetLabel('By Residence')

        self.Layout()

    def build_nhood_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.nhood_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                  size=(-1, -1),
                                                  style=flags)
        self.nhood_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.nhood_list_ctrl.SetColumns([
            olv.ColumnDefn('My Neighborhoods', 'left', 300, valueGetter='name'),
        ])
        nhoods = list(gbl.dataset.my_neighborhoods.values())
        self.nhood_list_ctrl.SetObjects(nhoods)
        self.nhood_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.nhood_select)
        layout.Add(self.nhood_list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def nhood_select(self, evt):
        nhood = self.nhood_list_ctrl.GetSelectedObject()
        if self.voter_panel.IsShown():
            self.voter_panel.load_voters(nhood.voters)
        else:
            self.residence_panel.load_voters(gbl.dataset.res_rex)

    def build_turnout_graph_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_turnout_graph_toolbar_panel(panel)
        lst = self.build_turnout_graph_list_panel(panel)

        layout.Add(tb, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def build_turnout_graph_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Turnout Graphs')
        layout.Add(lbl, 0, wx.ALL, 5)

        show_grf_btn = uil.toolbar_button(panel, 'Show Graph')
        layout.Add(show_grf_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_turnout_graph_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        grf_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                size=(-1, -1),
                                                style=flags)
        grf_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        grf_list_ctrl.SetColumns([
            olv.ColumnDefn('Turnout', 'left', 250, 'name'),
        ])
        grf_list_ctrl.SetObjects([
            {'name': 'All Voters'},
            {'name': 'Age Group'},
            {'name': 'Gender'}
        ])
        layout.Add(grf_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel

    def build_makeup_graph_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_makeup_graph_toolbar_panel(panel)
        lst = self.build_makeup_graph_list_panel(panel)

        layout.Add(tb, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def build_makeup_graph_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Composition Graphs')
        layout.Add(lbl, 0, wx.ALL, 5)

        show_grf_btn = uil.toolbar_button(panel, 'Show Graph')
        layout.Add(show_grf_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_makeup_graph_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        grf_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                size=(-1, -1),
                                                style=flags)
        grf_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        grf_list_ctrl.SetColumns([
            olv.ColumnDefn('Composition', 'left', 250, 'name')
        ])
        grf_list_ctrl.SetObjects([
            {'name': 'All Voters'},
            {'name': 'Age Group'},
            {'name': 'Gender'}
        ])
        layout.Add(grf_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel
