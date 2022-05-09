import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class StreetPickerPanel(wx.Panel):

    def __int__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_street_picker_tb_panel(self)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        lst_panel = self.build_street_picker_list_panel(self)
        layout.Add(lst_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

    def build_street_picker_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Pick a Street')
        layout.Add(lbl, 0, wx.ALL, 2)

        self.srch_ctrl = wx.SearchCtrl(panel, wx.ID_ANY,
                                       style=wx.TE_PROCESS_ENTER,
                                       name='srch_ctrl')
        self.srch_ctrl.ShowCancelButton(True)
        self.srch_ctrl.Bind(wx.EVT_CHAR, self.on_filter)
        self.srch_ctrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_filter_cancel)
        layout.Add(self.srch_ctrl, 1, wx.ALL | wx.EXPAND, 2)
        panel.SetSizer(layout)

        return panel

    def on_filter(self, evt):
        c = chr(evt.GetUnicodeKey())

        self.target = evt.EventObject.GetValue()
        if c == '\b':
            self.target = self.target[:-1]
        else:
            self.target += c

        self.street_picker_ctrl.SetFilter(olv.Filter.Predicate(self.filter_cond))
        self.street_picker_ctrl.RepopulateList()

        evt.Skip()

    def filter_cond(self, obj):
        return obj.name.lower().startswith(self.target.lower())

    def on_filter_cancel(self, evt):
        self.srch_ctrl.Clear()
        self.street_picker_ctrl.SetFilter(None)
        self.street_picker_ctrl.RepopulateList()
        evt.Skip()

    def build_street_picker_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.street_picker_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                     size=(-1, 500),
                                                     style=flags)
        self.street_picker_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.street_picker_ctrl.SetColumns([
            olv.ColumnDefn('Street', 'left', 300, 'name')
        ])
        self.street_picker_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
                                     self.on_street_picker_dbl_click)
        layout.Add(self.street_picker_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def on_street_picker_dbl_click(self, evt):
        self.add_street()

    def load_streets(self, streets):
        pass
        # self.street_picker_ctrl.SetObjects(streets)
