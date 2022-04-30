import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import controllers.neighborhood_controller as controller


class NeighborhoodPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        top_layout = wx.BoxSizer(wx.HORIZONTAL)

        nhoods_panel = self.build_nhoods_panel(self)
        top_layout.Add(nhoods_panel, 0, wx.ALL | wx.EXPAND, 5)

        streets_panel = self.build_streets_panel(self)
        top_layout.Add(streets_panel, 0, wx.ALL | wx.EXPAND, 5)

        street_list_panel = self.build_street_list_panel(self)
        top_layout.Add(street_list_panel, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(top_layout, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.config = controller.get_config()
        streets = controller.scrape_streets(self.config)
        self.load_street_picker(streets)

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

        new_nhood_btn = uil.toolbar_button(panel, 'New Neighborhood')
        new_nhood_btn.Bind(wx.EVT_BUTTON, self.new_nhood_btn_click)
        layout.Add(new_nhood_btn, 0, wx.ALL, 5)

        self.drop_nhood_btn = uil.toolbar_button(panel, 'Drop Neighborhood')
        layout.Add(self.drop_nhood_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

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
            olv.ColumnDefn('My Neighborhoods', 'left', valueGetter='name'),
        ])
        layout.Add(self.nhood_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)
        return panel

    def build_streets_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_streets_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        frm_panel = self.build_streets_list_panel(panel)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

        return panel

    def build_streets_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Streets')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.new_street_btn = uil.toolbar_button(panel, 'Add Street')
        layout.Add(self.new_street_btn, 0, wx.ALL, 5)

        self.drop_street_btn = uil.toolbar_button(panel, 'Drop Street')
        layout.Add(self.drop_street_btn, 0, wx.ALL, 5)

        self.save_street_btn = uil.toolbar_button(panel, 'Save Edits')
        layout.Add(self.save_street_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_streets_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.street_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                   size=(-1, -1),
                                                   style=flags)
        self.street_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.street_list_ctrl.SetColumns([
            olv.ColumnDefn('Street', 'left', 250, 'name'),
            olv.ColumnDefn('From', 'left', 50, 'lo'),
            olv.ColumnDefn('To', 'left', 50, 'hi'),
            olv.ColumnDefn('Side', 'left', 50, 'oe'),
        ])
        layout.Add(self.street_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def build_street_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_street_list_tb_panel(panel)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        frm_panel = self.build_street_list_list_panel(panel)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

        return panel

    def build_street_list_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.street_picker_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                   size=(-1, -1),
                                                   style=flags)
        self.street_picker_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.street_picker_ctrl.SetColumns([
            olv.ColumnDefn('Street', 'left', 300, 'name'),
        ])
        layout.Add(self.street_picker_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def build_street_list_tb_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Pick a Street')
        layout.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def load_street_picker(self, streets):
        d = [{'name': street} for street in streets]
        self.street_picker_ctrl.SetObjects(d)

    def add_to_nhood_list(self, nhood):
        self.nhood_list_ctrl.AddObjects([nhood])

    def clear_street_list(self):
        self.street_list_ctrl.ClearAll()

    def new_nhood_btn_click(self, evt):
        name = uil.get_txt_popup(self, 'New neighborhood name')
        if not name:
            return
        nhood = controller.new_nhood(self.config, name)
        self.add_to_nhood_list(nhood)
        self.clear_street_list()
