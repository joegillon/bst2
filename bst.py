import os
import wx
import logging.handlers
import configparser
from models.dataset import Dataset
import globals as gbl
from views.main_window import MainWindow


def get_config():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    state = parser['Locale']['state']
    state_name = parser['Locale']['state_name']
    city = parser['Locale']['city']
    ballot_date = parser['Ballots']['date']

    cwd = os.getcwd()

    return {
        'state': state, 'state_name': state_name,
        'city': city, 'ballot_date': ballot_date,
        'app_path': cwd
    }


def main():
    app = wx.App()

    gbl.dataset = Dataset()

    main_window = MainWindow(gbl.config['state_name'])

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

    gbl.config = get_config()

    main()
