import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from controllers.elections_controller import ElectionsController


class ElectionsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_elections_toolbar_panel(self)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        lst_panel = self.build_elections_lists_panel(self)
        layout.Add(lst_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.controller = ElectionsController(self)

    def build_elections_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Elections')
        layout.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_elections_lists_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        state_list_layout = wx.BoxSizer(wx.VERTICAL)
        state_list_layout.Add(wx.Size(-1, 6))

        state_list_hdr_layout = wx.BoxSizer(wx.HORIZONTAL)

        state_lbl = uil.toolbar_label(panel, 'State Elections')
        state_list_hdr_layout.Add(state_lbl, 0, wx.ALL, 5)

        self.state_cnt_lbl = uil.toolbar_label(panel, 'Number of Elections: ')
        self.state_cnt_lbl.SetForegroundColour('white')
        state_list_hdr_layout.Add(self.state_cnt_lbl, 0, wx.ALL, 5)

        self.state_score_lbl = uil.toolbar_label(panel, 'Possible Score: ')
        self.state_score_lbl.SetForegroundColour('white')
        state_list_hdr_layout.Add(self.state_score_lbl, 0, wx.ALL, 5)

        state_list_layout.Add(state_list_hdr_layout, 0, wx.ALL, 5)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER
        self.state_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                  size=(-1, -1),
                                                  sortable=False,
                                                  style=flags)
        self.state_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.state_list_ctrl.SetColumns([
            olv.ColumnDefn('Date', 'left', valueGetter='date'),
            olv.ColumnDefn('Description', 'left', valueGetter='description'),
            olv.ColumnDefn('Eligible Byr', 'left', 80, valueGetter='birth_yr'),
            olv.ColumnDefn('Value', 'left', 50, valueGetter='score'),
        ])
        self.state_list_ctrl.AutoSizeColumns()
        state_list_layout.Add(self.state_list_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        layout.Add(state_list_layout, 1, wx.ALL | wx.EXPAND, 5)

        btn_layout = wx.BoxSizer(wx.VERTICAL)
        btn_layout.Add(wx.Size(-1, 46))

        self.drop_elections_btn = uil.toolbar_button(panel, 'Drop')
        btn_size = self.drop_elections_btn.GetSize()

        self.all_elections_btn = uil.toolbar_button(panel, 'All')
        self.all_elections_btn.SetSize(btn_size)
        btn_layout.Add(self.all_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

        self.to_my_elections_btn = uil.toolbar_button(panel, '=>')
        self.to_my_elections_btn.SetSize(btn_size)
        btn_layout.Add(self.to_my_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

        btn_layout.Add(self.drop_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(btn_layout, 0, wx.ALL, 5)

        my_list_layout = wx.BoxSizer(wx.VERTICAL)

        my_list_hdr_layout = wx.BoxSizer(wx.HORIZONTAL)

        my_lbl = uil.toolbar_label(panel, 'My Elections')
        my_list_hdr_layout.Add(my_lbl, 0, wx.ALL, 5)

        self.my_cnt_lbl = uil.toolbar_label(panel, 'Number of Elections: ')
        self.my_cnt_lbl.SetForegroundColour('white')
        my_list_hdr_layout.Add(self.my_cnt_lbl, 0, wx.ALL, 5)

        self.my_score_lbl = uil.toolbar_label(panel, 'Possible Score: ')
        self.my_score_lbl.SetForegroundColour('white')
        my_list_hdr_layout.Add(self.my_score_lbl, 0, wx.ALL, 5)

        self.save_elections_btn = uil.toolbar_button(panel, 'Save')
        my_list_hdr_layout.Add(self.save_elections_btn, 0, wx.ALL, 5)

        my_list_layout.Add(my_list_hdr_layout, 0, wx.ALL, 5)

        self.my_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                               size=(-1, -1),
                                               sortable=False,
                                               style=flags)
        self.my_list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])
        self.my_list_ctrl.SetColumns([
            olv.ColumnDefn('Date', 'left', valueGetter='date'),
            olv.ColumnDefn('Description', 'left', valueGetter='description'),
            olv.ColumnDefn('Eligible Byr', 'left', 80, valueGetter='birth_yr'),
            olv.ColumnDefn('Value', 'left', 50, valueGetter='score'),
        ])
        self.my_list_ctrl.AutoSizeColumns()
        self.my_list_ctrl.SortBy(0, ascending=False)
        my_list_layout.Add(self.my_list_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        layout.Add(my_list_layout, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def get_state_elections(self):
        return self.state_list_ctrl.GetObjects()

    def get_selected_state_elections(self):
        return self.state_list_ctrl.GetSelectedObjects()

    def set_state_cnt_lbl(self, cnt):
        self.state_cnt_lbl.SetLabel('Number of Elections: %d' % cnt)

    def set_state_score_lbl(self, score):
        self.state_score_lbl.SetLabel('Possible Score: %d' % score)

    def set_state_elections(self, elections):
        self.state_list_ctrl.SetObjects(elections)
        cnt, score = self.cnt_score(elections)
        self.set_state_cnt_lbl(cnt)
        self.set_state_score_lbl(score)

    def get_my_elections(self):
        return self.my_list_ctrl.GetObjects()

    def set_my_elections(self, elections):
        self.my_list_ctrl.SetObjects(elections)
        cnt, score = self.cnt_score(elections)
        self.set_my_cnt_score(cnt, score)

    def set_my_cnt_score(self, cnt, score):
        self.set_my_cnt_lbl(cnt)
        self.set_my_score_lbl(score)

    def get_my_score(self):
        txt = self.my_score_lbl.GetLabel()
        parts = txt.split(': ')
        return int(parts[1])

    def get_my_cnt(self):
        txt = self.my_cnt_lbl.GetLabel()
        parts = txt.split(': ')
        return int(parts[1])

    def set_my_cnt_lbl(self, cnt):
        self.my_cnt_lbl.SetLabel('Number of Elections: %d' % cnt)

    def set_my_score_lbl(self, score):
        self.my_score_lbl.SetLabel('Possible Score: %d' % score)

    def drop_elections(self):
        elections = self.my_list_ctrl.GetSelectedObjects()
        self.my_list_ctrl.RemoveObjects(elections)

        cnt, score = self.cnt_score(elections)
        cnt = self.get_my_cnt() - cnt
        score = self.get_my_score() - score
        self.set_my_cnt_score(cnt, score)

    def add_elections(self):
        state_elections = self.state_list_ctrl.GetSelectedObjects()
        state_elections = [e for e in state_elections if not self.election_in_my(e)]
        self.my_list_ctrl.AddObjects(state_elections)

        cnt, score = self.cnt_score(state_elections)
        cnt += self.get_my_cnt()
        score += self.get_my_score()
        self.set_my_cnt_score(cnt, score)

    def election_in_my(self, election):
        return self.my_list_ctrl.GetIndexOf(election) != -1

    def cnt_score(self, elections):
        score = 0
        for election in elections:
            score += int(election.score)
        return len(elections), score
