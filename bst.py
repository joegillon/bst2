import wx
import logging.handlers
from models.dataset import Dataset
import globals as gbl
from views.main_window import MainWindow


def main():
    app = wx.App()

    gbl.dataset = Dataset()

    main_window = MainWindow()

    app.MainLoop()


if __name__ == '__main__':
    smtp_handler = logging.handlers.SMTPHandler(
        mailhost=('smtp.gmail.com', 465),
        fromaddr='joe.gillon1@gmail.com',
        toaddrs=['joe.gillon44@gmail.com'],
        subject='Bluestreets Exception'
    )
    smtp_handler.setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.addHandler(smtp_handler)

    main()
