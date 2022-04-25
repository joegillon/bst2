import csv
import wx
from models.voter import Voter


class VoterController(object):

    def __init__(self, view):
        self.view = view
        self.voters = None
        self.init_view()

    def init_view(self):
        self.view.select_btn.Bind(wx.EVT_BUTTON,
                                  self.select_btn_click)

        self.view.save_btn.Bind(wx.EVT_BUTTON,
                                self.save_btn_click)

        self.view.open_btn.Bind(wx.EVT_BUTTON,
                                self.open_btn_click)

        self.view.print_btn.Bind(wx.EVT_BUTTON,
                                 self.print_btn_click)

        self.view.deselect_btn.Bind(wx.EVT_BUTTON,
                                    self.deselect_btn_click)

    def load_voters(self, nhood):
        self.voters = Voter.get(nhood)
        election_cols = []
        for col in self.voters[0].__dict__:
            if col[0] == '2':
                election_cols.append(col)

        self.view.add_election_cols(election_cols)
        self.view.load_voters(self.voters)
        self.view.addr_sort_asc = True

    def select_btn_click(self, evt):
        self.view.filter()

    def save_btn_click(self, evt):
        with wx.FileDialog(self.view, 'Save List',
                           wildcard='List files (*.csv)|*.csv',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dlg.GetPath()
            try:
                with open(pathname, 'w', newline='') as file:
                    self.save_list(file)
            except IOError:
                wx.MessageDialog(self.view, 'Unable to save to %s' % pathname).ShowModal()

    def save_list(self, file):
        objs = self.view.get_list()
        flds = list(objs[0].__dict__.keys())
        wtr = csv.DictWriter(file, fieldnames=flds)
        wtr.writeheader()
        for obj in objs:
            wtr.writerow(obj.__dict__)

    def open_btn_click(self, evt):
        with wx.FileDialog(self.view, 'Open Saved List',
                           wildcard='List files (*.csv)|*.csv',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dlg.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.load_file(file)
            except IOError:
                wx.MessageDialog(self.view, 'Unable to open to %s' % pathname).ShowModal()

    def load_file(self, file):
        objs = []
        rdr = csv.DictReader(file)
        for row in rdr:
            objs.append(Voter(row))

        self.view.load_my_list(objs)

    def print_btn_click(self, evt):
        dlg = wx.MessageDialog(self.view, 'This will print the currently visible rows', 'Promises').ShowModal()

    def deselect_btn_click(self, evt):
        self.view.load_voters(self.voters)
        self.view.default_sort()

    def menu_btn_click(self, evt):
        pos = evt.EventObject.GetPosition()
        self.view.show_turnout_menu(pos)
