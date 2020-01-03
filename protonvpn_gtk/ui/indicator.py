import os

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

CURRDIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(CURRDIR, '../../icons')
ICON = os.path.join(ICON_DIR, 'proto.png')


class Indicator:

    def __init__(self, root):
        self.app = root
        self.ind = appindicator.Indicator.new(
            self.app.name,
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_icon_full(ICON, 'protonvpn')
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()
        item = Gtk.MenuItem()
        item.set_label("Status")
        item.connect("activate", self.app.main_win.cb_show)
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.cb_exit, '')
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def cb_exit(self, w, data):
        Gtk.main_quit()
