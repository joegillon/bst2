import wx
import dao


class ImportController(object):

    def __init__(self, view):
        self.view = view
        self.init_view()

    def init_view(self):
        self.view.import_sos_elections_btn.Bind(wx.EVT_BUTTON,
                                                self.import_sos_elections_btn_click)
        self.view.import_sos_voters_btn.Bind(wx.EVT_BUTTON,
                                             self.import_sos_voters_btn_click)
        self.view.import_bst_btn.Bind(wx.EVT_BUTTON, self.import_bst_btn_click)

    def import_sos_elections_btn_click(self, evt):
        title = 'Import SoS Elections File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = self.view.get_file_path(title, wildcard)

        try:
            with open(path, 'r') as file:
                self.import_sos_elections(file)
        except IOError:
            wx.MessageDialog(self.view, 'Unable to open to %s' % path).ShowModal()

    def import_sos_voters_btn_click(self, evt):
        title = 'Import SoS Voters File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = self.view.get_file_path(title, wildcard)

        try:
            with open(path, 'r') as file:
                self.import_sos_voters(file)
        except IOError:
            wx.MessageDialog(self.view, 'Unable to open to %s' % path).ShowModal()

    def import_bst_btn_click(self, evt):
        title = 'Import Bluestreets Voters File'
        wildcard = 'Bluestreets files (*.csv)|*.csv'
        path = self.view.get_file_path(title, wildcard)

        try:
            with open(path, 'r') as file:
                self.import_bst_voters(file)
        except IOError:
            wx.MessageDialog(self.view, 'Unable to open to %s' % path).ShowModal()

    def import_sos_elections(self, file):
        # msg = 'This will import SoS elections file %s' % file.name
        # wx.MessageDialog(self.view, msg, 'Promises').ShowModal()
        dao.elections_to_csv(file, self.view)

    def import_sos_voters(self, file):
        msg = 'This will import SoS voters file %s' % file.name
        wx.MessageDialog(self.view, msg, 'Promises').ShowModal()

    def import_bst_voters(self, file):
        msg = 'This will import Bluestreets file %s' % file.name
        wx.MessageDialog(self.view, msg, 'Promises').ShowModal()
