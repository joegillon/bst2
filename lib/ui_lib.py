import sys
import wx
import globals as gbl
from lib.custom_button import CustomButton


def toolbar_label(panel, text):
    font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_BOLD)
    lbl = wx.StaticText(panel, wx.ID_ANY, text)
    lbl.SetFont(font)
    lbl.SetForegroundColour('navy')
    return lbl


def toolbar_button(panel, label):
    btn = CustomButton(panel, wx.ID_ANY, label)
    font_normal = wx.Font(10,
                          wx.FONTFAMILY_DEFAULT,
                          wx.FONTSTYLE_NORMAL,
                          wx.FONTWEIGHT_BOLD)
    font_hover = wx.Font(10,
                         wx.FONTFAMILY_DEFAULT,
                         wx.FONTSTYLE_NORMAL,
                         wx.FONTWEIGHT_NORMAL)
    btn.set_font(font_normal, hover=font_hover)
    btn.set_foreground_color('#ffffff')
    btn.set_bg_color(gbl.COLOR_SCHEME['btnBg'])
    btn.set_cursor(wx.Cursor(wx.CURSOR_HAND))
    if gbl.COLOR_SCHEME['btnGrd']:
        btn.set_bg_gradient(gbl.COLOR_SCHEME['btnGrd'])
    btn.set_border((1, 'white', 1))
    btn.set_padding((5, 10, 5, 10))

    return btn


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_file_path(parent, title, wildcard, multiple=None):
    flags = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    if multiple:
        flags |= wx.FD_MULTIPLE
    with wx.FileDialog(parent, title, wildcard=wildcard, style=flags) as dlg:
        reply = dlg.ShowModal()
        if reply == wx.ID_OK:
            return dlg.GetPath()

    return None


def inform(parent, msg):
    wx.MessageDialog(parent, msg, 'Just so you know', wx.OK | wx.ICON_INFORMATION).ShowModal()


def confirm(parent, msg):
    dlg = wx.MessageDialog(parent, msg, 'Please confirm', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
    reply = dlg.ShowModal()
    return reply == wx.ID_OK


def oops(parent, msg):
    wx.MessageDialog(parent, msg, 'Oops!', wx.OK | wx.ICON_ERROR).ShowModal()
