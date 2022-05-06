import wx
import globals as gbl
import lib.ui_lib as uil


class StreetFormDlg(wx.Dialog):

    def __init__(self, parent, street):
        wx.Dialog.__init__(self, parent)
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        self.street = street

        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_tb_panel(panel)
        frm_panel = self.build_frm_panel(panel)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

    def build_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        name_lbl = uil.toolbar_label(panel, 'Neighborhood Street')
        name_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME['tbFg']))
        layout.Add(name_lbl, 0, wx.ALL, 5)

        btn_layout = wx.BoxSizer(wx.HORIZONTAL)

        cancel_btn = uil.toolbar_button(panel, 'Cancel')
        cancel_btn.Bind(wx.EVT_BUTTON, self.cancel_btn_click)
        btn_layout.Add(cancel_btn, 0, wx.ALL, 5)

        save_btn = uil.toolbar_button(panel, 'Save')
        save_btn.Bind(wx.EVT_BUTTON, self.save_btn_click)
        btn_layout.Add(save_btn, 0, wx.ALL, 5)

        layout.Add(btn_layout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_frm_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['frmBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        from_layout = wx.BoxSizer(wx.VERTICAL)
        from_lbl = uil.toolbar_label(panel, 'From')
        self.from_txt = wx.TextCtrl(panel, wx.ID_ANY, self.street.lo)
        from_layout.Add(from_lbl, 0, wx.ALL, 5)
        from_layout.Add(self.from_txt, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(from_layout, 0, wx.ALL, 5)

        thru_layout = wx.BoxSizer(wx.VERTICAL)
        thru_lbl = uil.toolbar_label(panel, 'Thru')
        self.thru_txt = wx.TextCtrl(panel, wx.ID_ANY, self.street.hi)
        thru_layout.Add(thru_lbl, 0, wx.ALL, 5)
        thru_layout.Add(self.thru_txt, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(thru_layout, 0, wx.ALL, 5)

        side_layout = wx.BoxSizer(wx.VERTICAL)
        side_lbl = uil.toolbar_label(panel, 'Side')
        choices = ['B', 'E', 'O']
        self.side_radio = wx.RadioBox(panel, wx.ID_ANY, label='',
                                      choices=choices)
        self.side_radio.SetSelection(choices.index(self.street.side))
        side_layout.Add(side_lbl, 0, wx.ALL, 5)
        side_layout.Add(self.side_radio, 0, wx.ALL, 5)

        layout.Add(side_layout, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def save_btn_click(self, evt):
        self.street.lo = self.from_txt.GetValue()
        self.street.hi = self.thru_txt.GetValue()
        self.street.side = self.side_radio.GetStringSelection()

        self.Close()

    def cancel_btn_click(self, evt):
        self.Close()
