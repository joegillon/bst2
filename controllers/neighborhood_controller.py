import wx
from models.neighborhood import Neighborhood
from models.graph import Graph
import lib.grf_lib as gfl


class NeighborhoodController(object):

    def __init__(self, view):
        self.view = view
        self.init_view()

    def init_view(self):
        self.view.new_nhood_btn.Bind(wx.EVT_BUTTON,
                                     self.new_nhood_click)
        self.view.drop_nhood_btn.Bind(wx.EVT_BUTTON,
                                      self.drop_nhood_click)
        self.view.new_street_btn.Bind(wx.EVT_BUTTON,
                                      self.new_street_click)
        self.view.drop_street_btn.Bind(wx.EVT_BUTTON,
                                       self.drop_street_click)
        self.view.save_street_btn.Bind(wx.EVT_BUTTON,
                                       self.save_street_click)
        self.view.show_grf_btn.Bind(wx.EVT_BUTTON,
                                    self.show_grf_click)

        grfs = Graph.get()
        self.view.load_grf_list(grfs)

        nhoods = Neighborhood.get()
        self.view.load_neighborhoods(nhoods)

    def new_nhood_click(self, evt):
        wx.MessageDialog(self.view, 'This will show form to create new neighborhood', 'Promises').ShowModal()

    def drop_nhood_click(self, evt):
        wx.MessageDialog(self.view, 'This will remove a neighborhood', 'Promises').ShowModal()

    def new_street_click(self, evt):
        wx.MessageDialog(self.view, 'This will add a new street to neighborhood', 'Promises').ShowModal()

    def drop_street_click(self, evt):
        wx.MessageDialog(self.view, 'This will remove a street from neighborhood', 'Promises').ShowModal()

    def save_street_click(self, evt):
        wx.MessageDialog(self.view, 'This will save any edits to neighborhood streets', 'Promises').ShowModal()

    def show_grf_click(self, evt):
        nhood = self.view.get_current_nhood()
        grf = self.view.get_grf_selections()
        choice = grf[0].name
        if choice == 'All Voters':
            gdf = gfl.all_gdf(nhood)
        elif choice == 'Gender':
            gdf = gfl.gender_gdf(nhood)
        elif choice == 'Age Group':
            gdf = gfl.age_gdf(nhood)
        else:
            gdf = gfl.party_gdf(nhood)

        self.draw(gdf)

    def draw(self, df):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_ylabel('Voters', fontsize=10)
        ax.set_xlabel('Elections', fontsize=10)
        df.T.plot(ax=ax, kind='bar', stacked=False)
        plt.show()
