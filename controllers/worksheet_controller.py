import wx
from controllers.neighborhood_controller import NeighborhoodController
from controllers.voter_controller import VoterController


class WorksheetController(object):

    def __init__(self, nhood_panel, voter_panel):
        self.nhood_panel = nhood_panel
        self.voter_panel = voter_panel
        self.nhood_controller = NeighborhoodController(nhood_panel)
        self.voter_controller = VoterController(voter_panel)

        self.init_view()

    def init_view(self):
        self.nhood_panel.nhood_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                              self.nhood_list_click)

        self.nhood_panel.select_neighborhood(0)

    def nhood_list_click(self, evt):
        self.nhood_panel.load_streets(evt.EventObject.GetSelectedObject().streets)
        nhood = evt.EventObject.GetSelectedObject().name.replace(' ', '_')
        self.voter_controller.load_voters(nhood)
