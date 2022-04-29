import wx
from views.elections_panel import ElectionsPanel
from views.worksheet_panel import WorksheetPanel
from views.import_panel import ImportPanel
from views.neighborhood_panel import NeighborhoodPanel


class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title='Bluestreets',
                          size=(1250, 650), pos=(20, 20))

        layout = wx.BoxSizer(wx.VERTICAL)

        notebook = wx.Notebook(self)

        elections_panel = ElectionsPanel(notebook)
        notebook.AddPage(elections_panel, 'Elections')

        # new_nhood_panel = NeighborhoodPanel(notebook)
        # notebook.AddPage(new_nhood_panel, 'Define Neighborhoods')

        # work_panel = WorksheetPanel(notebook)
        # notebook.AddPage(work_panel, 'Worksheet')

        import_panel = ImportPanel(notebook)
        notebook.AddPage(import_panel, 'Import Data')

        layout.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(layout)

        self.Show()
