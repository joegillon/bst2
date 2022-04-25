import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class NewNeighborhoodPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        # self.controller = controller

        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_nhoods_toolbar_panel(self)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        frm_panel = self.build_nhoods_frm_panel(self)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

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
