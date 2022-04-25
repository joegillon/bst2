import wx
from views.neighborhood_panel import NeighborhoodPanel
from views.voter_panel import VoterPanel
from controllers.worksheet_controller import WorksheetController
import globals as gbl


class WorksheetPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        nhood_panel = NeighborhoodPanel(self)
        layout.Add(nhood_panel, 0, wx.ALL | wx.EXPAND, 5)

        voter_panel = VoterPanel(self)
        layout.Add(voter_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.controller = WorksheetController(nhood_panel, voter_panel)
