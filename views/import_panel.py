import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from controllers.import_controller import ImportController


class ImportPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME['pnlBg'])

        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_import_toolbar_panel(self)
        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)

        prg_panel = self.build_import_progress_panel(self)
        layout.Add(prg_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

        self.controller = ImportController(self)

    def build_import_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Import Data')
        layout.Add(lbl, 0, wx.ALL, 5)

        self.import_sos_elections_btn = uil.toolbar_button(panel, 'Import SoS Elections')
        self.import_sos_elections_btn.SetName('SoS_elections')
        layout.Add(self.import_sos_elections_btn, 0, wx.ALL, 5)

        self.import_sos_voters_btn = uil.toolbar_button(panel, 'Import SoS Voters')
        self.import_sos_voters_btn.SetName('SoS_voters')
        layout.Add(self.import_sos_voters_btn, 0, wx.ALL, 5)

        self.import_bst_btn = uil.toolbar_button(panel, 'Import Bluestreets Voters')
        self.import_bst_btn.SetName('Bst')
        layout.Add(self.import_bst_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_import_progress_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])

        layout = wx.BoxSizer(wx.VERTICAL)

        self.prg_txt = wx.TextCtrl(panel, wx.ID_ANY,
                                   style=wx.TE_MULTILINE | wx.TE_READONLY)
        layout.Add(self.prg_txt, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def get_file_path(self, title, wildcard):
        with wx.FileDialog(self, title,
                           wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return None

            return dlg.GetPath()

    def log(self, msg):
        self.prg_txt.write(msg + '\n')
