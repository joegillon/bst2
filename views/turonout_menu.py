import wx


class TurnoutMenu(wx.Menu):

    def __init__(self, parent):
        super(TurnoutMenu, self).__init__()
        self.parent = parent

        all_item = wx.MenuItem(self, wx.ID_ANY,
                               text='All Voters', kind=wx.ITEM_NORMAL)
        self.Append(all_item)

        age_group_item = wx.MenuItem(self, wx.ID_ANY,
                                     text='Age Group', kind=wx.ITEM_NORMAL)
        self.Append(age_group_item)

        gender_item = wx.MenuItem(self, wx.ID_ANY,
                                  text='Gender', kind=wx.ITEM_NORMAL)
        self.Append(gender_item)

