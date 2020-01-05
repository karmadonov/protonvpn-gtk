from gi.repository import Gtk


class ServersWindow(Gtk.Window):

    def __init__(self, root):
        super().__init__()
        self.app = root
        self.set_title(f'{self.app.name} Servers')
        self.server_store = Gtk.ListStore(str, str)
        self.server_id = None
        self.protocol = 'UDP'

    def cb_show(self, w):
        self.resize(300, 200)
        country_store = Gtk.ListStore(str, str)
        countries = self.app.proton('get_countries')()
        for country_code in sorted(countries):
            country_store.append([countries[country_code]['name'],
                                  country_code])

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(country_combo, False, False, True)

        self.server_combo = Gtk.ComboBox.new_with_model(self.server_store)
        self.server_combo.connect("changed", self.on_server_combo_changed)
        vbox.pack_start(self.server_combo, False, False, True)

        protocol_store = Gtk.ListStore(str, str)
        protocol_store.append(['UDP (Better Speed)', 'UDP'])
        protocol_store.append(['TCP (Better Reliability)', 'TCP'])
        self.protocol_combo = Gtk.ComboBox.new_with_model(protocol_store)
        self.protocol_combo.set_active(0)
        self.protocol_combo.connect("changed", self.on_protocol_combo_changed)
        renderer_text = Gtk.CellRendererText()
        self.protocol_combo.pack_start(renderer_text, True)
        self.protocol_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(self.protocol_combo, False, False, True)

        self.button = Gtk.Button.new_with_mnemonic("_Connect")
        self.button.connect("clicked", self.on_connect_clicked)
        self.button.set_sensitive(False)
        vbox.pack_start(self.button, True, True, 0)

        self.add(vbox)
        self.show_all()

    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            country_code = model[tree_iter][1]
            self.server_store.clear()
            servers = self.app.get_protonvpn_method('get_servers_for_country')(
                country_code)
            for server_id, server in sorted(servers.items(),
                                            key=lambda item: item[1]['Load']):
                self.server_store.append([server['Name'], server_id])
            self.server_combo.set_model(self.server_store)
            renderer_text = Gtk.CellRendererText()
            self.server_combo.pack_start(renderer_text, True)
            self.server_combo.add_attribute(renderer_text, "text", 0)

    def on_server_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            server_id = model[tree_iter][1]
            self.server_id = server_id
            self.button.set_sensitive(True)

    def on_protocol_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            protocol = model[tree_iter][1]
            self.protocol = protocol

    def on_connect_clicked(self, button):
        self.app.get_protonvpn_method('connect')(self.server_id, self.protocol)
        self.close()
