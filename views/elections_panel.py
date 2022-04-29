import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import controllers.elections_controller as controller


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

        self.set_state_elections(controller.get_state_elections())
        self.set_my_elections(controller.get_my_elections())

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

        all_elections_btn = uil.toolbar_button(panel, 'All')
        all_elections_btn.Bind(wx.EVT_BUTTON, self.all_elections_btn_click)
        btn_layout.Add(all_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

        to_my_elections_btn = uil.toolbar_button(panel, '=>')
        to_my_elections_btn.Bind(wx.EVT_BUTTON, self.to_my_elections_btn_click)
        btn_layout.Add(to_my_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

        drop_elections_btn = uil.toolbar_button(panel, 'Drop')
        drop_elections_btn.Bind(wx.EVT_BUTTON, self.drop_elections_btn_click)
        btn_layout.Add(drop_elections_btn, 0, wx.ALL | wx.EXPAND, 5)

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

        save_elections_btn = uil.toolbar_button(panel, 'Save')
        save_elections_btn.Bind(wx.EVT_BUTTON, self.save_elections_btn_click)
        my_list_hdr_layout.Add(save_elections_btn, 0, wx.ALL, 5)

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

    def all_elections_btn_click(self, evt):
        self.my_list_ctrl.SetObjects(self.state_list_ctrl.GetObjects())
        self.set_my_labels(self.get_lbl_values('state'))

    def to_my_elections_btn_click(self, evt):
        selected_elections = self.state_list_ctrl.GetSelectedObjects()
        selected_elections = [e for e in selected_elections if not self.election_in_my(e)]
        self.my_list_ctrl.AddObjects(selected_elections)

        cnt, score = self.calc_cnt_score(selected_elections)
        my_lbl_values = self.get_lbl_values('my')
        cnt += my_lbl_values[0]
        score += my_lbl_values[1]
        self.set_my_labels([cnt, score])

    def drop_elections_btn_click(self, evt):
        selected_elections = self.my_list_ctrl.GetSelectedObjects()
        self.my_list_ctrl.RemoveObjects(selected_elections)

        cnt, score = self.calc_cnt_score(selected_elections)
        cnt = self.get_my_cnt() - cnt
        score = self.get_my_score() - score
        self.set_my_labels([cnt, score])

    def get_lbl_values(self, whose):
        if whose == 'state':
            cnt_lbl = self.state_cnt_lbl
            score_lbl = self.state_score_lbl
        else:
            cnt_lbl = self.my_cnt_lbl
            score_lbl = self.my_score_lbl

        txt = cnt_lbl.GetLabel()
        cnt = int(txt.split(': ')[1])
        txt = score_lbl.GetLabel()
        score = int(txt.split(': ')[1])

        return [cnt, score]

    def set_state_elections(self, elections):
        self.state_list_ctrl.SetObjects(elections)
        cnt, score = self.calc_cnt_score(elections)
        self.state_cnt_lbl.SetLabel('Number of Elections: %d' % cnt)
        self.state_score_lbl.SetLabel('Possible Score: %d' % score)

    def get_my_elections(self):
        return self.my_list_ctrl.GetObjects()

    def set_my_elections(self, elections):
        self.my_list_ctrl.SetObjects(elections)
        cnt, score = self.calc_cnt_score(elections)
        self.set_my_labels([cnt, score])

    def set_my_labels(self, values):
        self.set_my_cnt_lbl(values[0])
        self.set_my_score_lbl(values[1])

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

    def election_in_my(self, election):
        return self.my_list_ctrl.GetIndexOf(election) != -1

    def calc_cnt_score(self, elections):
        score = 0
        for election in elections:
            score += int(election.score)
        return len(elections), score

    def save_elections_btn_click(self, evt):
        elections = self.get_my_elections()
        controller.save(elections)
        wx.MessageDialog(self, 'Done!', 'Tada!').ShowModal()
