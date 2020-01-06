from gi.repository import Gtk

from .status import StatusWindow
from .servers import ServersWindow
from .indicator import Indicator

from protonvpn_gtk.utils.protonlib.core import ProtonVPN


class MyApp(Gtk.Application):

    def get_protonvpn_method(self, method: str):
        return getattr(self.protonvpn, method)

    def proton(self, method: str):
        return lambda _=None: self.get_protonvpn_method(method)()

    def __init__(self, app_name):
        super().__init__()
        self.name = app_name
        self.protonvpn = ProtonVPN()
        self.main_win = StatusWindow(self)
        self.servers_win = ServersWindow(self)
        self.indicator = Indicator(self)

    def run(self):
        Gtk.main()
