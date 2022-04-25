import wx
from views.main_window import MainWindow


def main():
    app = wx.App()

    main_window = MainWindow()
    main_window.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
