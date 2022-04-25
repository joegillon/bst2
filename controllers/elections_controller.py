import wx
from models.election import Election


class ElectionsController(object):

    def __init__(self, view):
        self.view = view
        self.init_view()

    def init_view(self):
        bst_elections = Election.get_bst()
        self.view.set_state_elections(bst_elections)
        my_elections = Election.get_my()
        self.view.set_my_elections(my_elections)

        self.view.all_elections_btn.Bind(wx.EVT_BUTTON, self.all_elections_btn_click)
        self.view.save_elections_btn.Bind(wx.EVT_BUTTON, self.save_elections_btn_click)
        self.view.drop_elections_btn.Bind(wx.EVT_BUTTON, self.drop_elections_btn_click)
        self.view.to_my_elections_btn.Bind(wx.EVT_BUTTON, self.to_my_elections_btn_click)

    def all_elections_btn_click(self, evt):
        objs = self.view.get_state_elections()
        self.view.set_my_elections(objs)

    def save_elections_btn_click(self, evt):
        objs = self.view.get_my_elections()
        Election.save(objs)
        wx.MessageDialog(self.view, 'Done!', 'Tada!').ShowModal()

    def drop_elections_btn_click(self, evt):
        self.view.drop_elections()

    def to_my_elections_btn_click(self, evt):
        self.view.add_elections()
