from gi.repository import Gtk

from protonvpn_gtk.utils.core import ProtonVPN


class StatusWindow(Gtk.Window):

    def __init__(self, root):
        super().__init__()
        self.app = root
        self.set_title(f'{self.app.name} Status')

    def cb_show(self, w):
        self.resize(300, 200)
        self.wbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.wbox.set_homogeneous(False)
        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.LEFT)
        self.wbox.pack_start(self.label, True, True, 0)
        self.add(self.wbox)
        proton = ProtonVPN()
        status = proton.status()
        self.label.set_text(status)
        self.show_all()
