import sys
import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from views.street_dialog import StreetFormDlg
import controllers.neighborhood_controller as controller


class NeighborhoodPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        street_picker_layout = wx.BoxSizer(wx.VERTICAL)
        street_picker_panel = self.build_street_picker_panel(self)
        street_picker_layout.Add(street_picker_panel, 1, wx.ALL | wx.EXPAND, 2)

        nhood_layout = wx.BoxSizer(wx.VERTICAL)

        top_layout = wx.BoxSizer(wx.HORIZONTAL)
        streets_panel = self.build_streets_panel(self)
        nhoods_panel = self.build_nhoods_panel(self)
        top_layout.Add(streets_panel, 0, wx.ALL | wx.EXPAND, 2)
        top_layout.Add(nhoods_panel, 0, wx.ALL | wx.EXPAND, 2)

        bottom_layout = wx.BoxSizer(wx.VERTICAL)
        prg_panel, self.prg_ctrl = uil.build_import_progress_panel(self)
        bottom_layout.Add(prg_panel, 1, wx.ALL | wx.EXPAND, 2)

        nhood_layout.Add(top_layout, 0, wx.ALL | wx.EXPAND, 2)
        nhood_layout.Add(bottom_layout, 1, wx.ALL | wx.EXPAND, 2)

        layout.Add(street_picker_layout, 0, wx.ALL | wx.EXPAND, 2)
        layout.Add(nhood_layout, 0, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(layout)

        sys.stdout = self.prg_ctrl
        streets = controller.get_city_streets()
        self.street_picker_ctrl.SetObjects(streets)

    def build_street_picker_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_street_picker_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        lst_panel = self.build_street_picker_list_panel(panel)
        layout.Add(lst_panel, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

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

    def build_streets_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_streets_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        lst_panel = self.build_streets_list_panel(panel)
        layout.Add(lst_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

        return panel

    def build_streets_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Streets')
        layout.Add(lbl, 0, wx.ALL, 5)

        add_street_btn = uil.toolbar_button(panel, 'Add')
        add_street_btn.Bind(wx.EVT_BUTTON, self.on_add_street_btn_click)
        layout.Add(add_street_btn, 0, wx.ALL, 5)

        edit_street_btn = uil.toolbar_button(panel, 'Edit')
        edit_street_btn.Bind(wx.EVT_BUTTON, self.on_edit_street_btn_click)
        layout.Add(edit_street_btn, 0, wx.ALL, 5)

        drop_street_btn = uil.toolbar_button(panel, 'Drop')
        drop_street_btn.Bind(wx.EVT_BUTTON, self.on_drop_street_btn_click)
        layout.Add(drop_street_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def on_add_street_btn_click(self, evt):
        self.add_street()

    def on_edit_street_btn_click(self, evt):
        self.edit_street()

    def on_drop_street_btn_click(self, evt):
        if not uil.confirm(self, 'Are you sure you want to drop this street?'):
            return
        obj = self.street_list_ctrl.GetSelectedObject()
        if not obj:
            return
        self.street_list_ctrl.RemoveObject(obj)

    def build_streets_list_panel(self, parent):
        import wx.grid

        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        self.street_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                   size=(-1, -1),
                                                   style=flags)
        self.street_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.street_list_ctrl.SetColumns([
            olv.ColumnDefn('Street', 'left', 250, 'name'),
            olv.ColumnDefn('From', 'left', 50, 'lo'),
            olv.ColumnDefn('To', 'left', 50, 'hi'),
            olv.ColumnDefn('Side', 'left', 50, 'side'),
        ])
        self.street_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
                                   self.on_street_list_dbl_click)
        layout.Add(self.street_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def on_street_list_dbl_click(self, evt):
        self.edit_street()

    def build_nhoods_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb = self.build_nhoods_tb_panel(panel)
        layout.Add(tb, 0, wx.EXPAND | wx.ALL, 5)

        lst = self.build_nhoods_list_panel(panel)
        layout.Add(lst, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_nhoods_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Neighborhoods')
        layout.Add(lbl, 0, wx.ALL, 5)

        add_nhood_btn = uil.toolbar_button(panel, 'Add')
        add_nhood_btn.Bind(wx.EVT_BUTTON, self.on_add_nhood_btn_click)
        layout.Add(add_nhood_btn, 0, wx.ALL, 5)

        drop_nhood_btn = uil.toolbar_button(panel, 'Drop')
        drop_nhood_btn.Bind(wx.EVT_BUTTON, self.on_drop_nhood_btn_click)
        layout.Add(drop_nhood_btn, 0, wx.ALL, 5)

        save_nhood_btn = uil.toolbar_button(panel, 'Save')
        save_nhood_btn.Bind(wx.EVT_BUTTON, self.on_save_nhood_btn_click)
        layout.Add(save_nhood_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def on_add_nhood_btn_click(self, evt):
        name = uil.get_txt_popup(self, 'New neighborhood name')
        if not name:
            return

        streets = self.street_list_ctrl.GetObjects()

        sys.stdout = self.prg_ctrl
        nhood = controller.new_nhood(name, streets)

        self.add_to_nhood_list(nhood)
        self.clear_street_list()

    def on_drop_nhood_btn_click(self, evt):
        uil.inform(self, 'Not yet implemented')

    def on_save_nhood_btn_click(self, evt):
        uil.inform(self, 'Not yet implemented')

    def build_nhoods_list_panel(self, parent):
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
        layout.Add(self.nhood_list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel

    def add_to_nhood_list(self, nhood):
        self.nhood_list_ctrl.AddObject(nhood)
        self.nhood_list_ctrl.SelectObject(nhood)

    def clear_street_list(self):
        self.street_list_ctrl.ClearAll()

    def add_street(self):
        street = self.street_picker_ctrl.GetSelectedObject()
        if not street:
            uil.inform(self, 'You need to pick a street first!')
            return

        if not street.house_nums:
            controller.get_house_nums(street)

        dlg = StreetFormDlg(self, street)
        dlg.ShowModal()

        self.street_list_ctrl.AddObject(street)
        self.street_list_ctrl.SelectObject(street)

    def edit_street(self):
        street = self.street_list_ctrl.GetSelectedObject()
        if not street:
            uil.inform(self, 'You need to pick a street first!')
            return

        dlg = StreetFormDlg(self, street)
        dlg.ShowModal()

        self.street_list_ctrl.RefreshObject(street)
