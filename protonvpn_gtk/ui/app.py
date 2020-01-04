from gi.repository import Gtk

from .status import StatusWindow
from .indicator import Indicator

from protonvpn_gtk.utils.core import ProtonVPN


class MyApp(Gtk.Application):

    @staticmethod
    def proton(method: str):
        return lambda _=None: getattr(ProtonVPN(), method)()

    def __init__(self, app_name):
        super().__init__()
        self.name = app_name
        self.main_win = StatusWindow(self)
        self.indicator = Indicator(self)

    def run(self):
        Gtk.main()
