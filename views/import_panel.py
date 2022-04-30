import sys
import wx
import globals as gbl
import lib.ui_lib as uil
import controllers.import_controller as controller


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

    def build_import_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['tbBg'])

        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.toolbar_label(panel, 'Import Data')
        layout.Add(lbl, 0, wx.ALL, 5)

        import_sos_elections_btn = uil.toolbar_button(panel, 'Import SoS Elections')
        import_sos_elections_btn.SetName('SoS_elections')
        import_sos_elections_btn.Bind(wx.EVT_BUTTON, self.import_sos_elections_btn_click)
        layout.Add(import_sos_elections_btn, 0, wx.ALL, 5)

        import_sos_voters_btn = uil.toolbar_button(panel, 'Import SoS Voters')
        import_sos_voters_btn.SetName('SoS_voters')
        import_sos_voters_btn.Bind(wx.EVT_BUTTON, self.import_sos_voters_btn_click)
        layout.Add(import_sos_voters_btn, 0, wx.ALL, 5)

        import_sos_hx_btn = uil.toolbar_button(panel, 'Import SoS Voter History')
        import_sos_hx_btn.SetName('SoS_hx')
        import_sos_hx_btn.Bind(wx.EVT_BUTTON, self.import_sos_hx_btn_click)
        layout.Add(import_sos_hx_btn, 0, wx.ALL, 5)

        import_bst_voters_btn = uil.toolbar_button(panel, 'Import Bluestreets Voters')
        import_bst_voters_btn.SetName('Bst')
        import_bst_voters_btn.Bind(wx.EVT_BUTTON, self.import_bst_voters_btn_click)
        layout.Add(import_bst_voters_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_import_progress_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME['lstHdr'])

        layout = wx.BoxSizer(wx.VERTICAL)

        prg_txt = wx.TextCtrl(panel, wx.ID_ANY,
                              style=wx.TE_MULTILINE | wx.TE_READONLY)
        sys.stdout = prg_txt
        layout.Add(prg_txt, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def import_sos_elections_btn_click(self, evt):
        title = 'Import SoS Elections File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = uil.get_file_path(self, title, wildcard)

        if not path:
            return

        try:
            with open(path, 'r') as file:
                controller.import_sos_elections(file)
        except Exception as ex:
            uil.oops(self, '%s. Maybe this is not an elections file?' % str(ex))

    def import_sos_voters_btn_click(self, evt):
        title = 'Import SoS Voters File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = uil.get_file_path(self, title, wildcard)

        if not path:
            return

        try:
            if not self.confirm_import():
                return
            with open(path, 'r') as file:
                has_hx_file = controller.import_sos_voters(file)
        except Exception as ex:
            uil.oops(self, '%s. Maybe this is not a voter file?' % str(ex))

        if has_hx_file:
            self.import_hx()

    def confirm_import(self):
        msg = ("If this is a state file, it will be a few minutes. "
               "You should do nothing on this computer until it's done.")
        return uil.confirm(self, msg)

    def import_sos_hx_btn_click(self, evt):
        title = 'Import SoS Voter History File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = uil.get_file_path(self, title, wildcard)

        if not path:
            return

        try:
            if not self.confirm_import():
                return
            with open(path, 'r') as file:
                controller.import_hx(file)
        except Exception as ex:
            uil.oops(self, '%s. Maybe this is not a history file?' % str(ex))

    def import_hx(self):
        msg = 'Looks like you need to import a history file as well.'
        uil.inform(self, msg)

        title = 'Import SoS History File'
        wildcard = 'SoS files (*.csv)|*.*'
        path = uil.get_file_path(self, title, wildcard)

        if not path:
            return

        try:
            with open(path, 'r') as path:
                controller.import_hx(path)
        except Exception as ex:
            uil.oops(self, '%s. Maybe this is not a history file?' % str(ex))

    def import_bst_voters_btn_click(self, evt):
        uil.inform(self, 'Not yet available - working on it.')

    # def log_progress(self, msg):
    #     self.prg_txt.write(msg + '\n')
