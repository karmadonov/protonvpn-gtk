import configparser
import datetime
import time

from protonvpn_cli.connection import (
    manage_dns,
    manage_ipv6,
    manage_killswitch,
    fastest,
)
from protonvpn_cli.constants import CONFIG_FILE, CONFIG_DIR
from protonvpn_cli.utils import (
    get_ip_info,
    get_country_name,
    get_servers,
    get_server_value,
    pull_server_data,
)

from .system import (
    is_connected,
    is_killswitch_active,
    is_server_reachable,
    kill_openvpn,
)


class ProtonVPN:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        self.config = {s: dict(config.items(s)) for s in config.sections()}

    def _check_configs(self) -> bool:
        if 'USER' not in self.config:
            return False

        if self.config['USER'].get("initialized", None) != '1':
            return False

        required_props = {"username", "tier", "default_protocol",
                          "dns_leak_protection", "custom_dns"}
        return not bool(required_props - self.config['USER'].keys())

    @staticmethod
    def is_connected() -> bool:
        """ Return connection status """
        return is_connected()

    def status(self) -> str:
        """ Return the current VPN status.

            Showing connection status (connected/disconnected),
            current IP, server name, country, server load
        """
        if not self._check_configs():
            return 'Settings problem. Please run "protonvpn init".'

        killswitch_active = is_killswitch_active(CONFIG_DIR)
        if not is_connected():
            msgs = ['Not connected']
            if killswitch_active:
                msgs.append('Kill Switch is currently active.')
            ip, isp = get_ip_info()
            msgs.extend((f'IP: {ip}', f'ISP: {isp}'))
            return '\n'.join(msgs)

        pull_server_data()

        metadata = self.config.get('metadata', {})
        current_server = metadata.get("connected_server", None)
        current_protocol = metadata.get("connected_proto", None)
        dns_server = metadata.get("dns_server", None)
        if not metadata or \
                not all((current_server, current_protocol, dns_server)):
            return 'Please connect with "protonvpn connect" first.'

        if not is_server_reachable(dns_server):
            msgs = ('Could not reach VPN server',
                    'You may want to reconnect with "protonvpn reconnect"')
            return '\n'.join(msgs)

        servers = get_servers()
        subs = [s["Servers"] for s in servers if s["Name"] == current_server]
        server_ips = [subserver["ExitIP"] for subserver in subs[0]]

        ip, isp = get_ip_info()

        if ip not in server_ips:
            msgs = ("Your IP was not found in last Servers IPs",
                    "Maybe you're not connected to a ProtonVPN Server")
            return '\n'.join(msgs)

        all_features = {0: "Normal", 1: "Secure-Core", 2: "Tor", 4: "P2P"}

        country_code = get_server_value(current_server, "ExitCountry", servers)
        country = get_country_name(country_code)
        city = get_server_value(current_server, "City", servers)
        load = get_server_value(current_server, "Load", servers)
        feature = get_server_value(current_server, "Features", servers)
        last_connection = metadata.get("connected_time")
        connection_time = time.time() - int(last_connection)

        killswitch_status = "Enabled" if killswitch_active else "Disabled"
        connection_time = str(datetime.timedelta(
            seconds=connection_time)).split(".")[0]

        msgs = (
            "Status: Connected",
            f"Time: {connection_time}",
            f"IP: {ip}",
            f"Server: {current_server}",
            f"Features: {all_features[feature]}",
            f"Protocol: {current_protocol.upper()}",
            f"Kill Switch: {killswitch_status}",
            f"Country: {country}",
            f"City: {city}",
            f"Load: {load}",
        )
        return '\n'.join(msgs)

    @staticmethod
    def disconnect():
        """Disconnect from VPN."""
        if is_connected():
            connected = kill_openvpn()

            timer_start = time.time()
            while connected:
                if time.time() - timer_start <= 5:
                    connected = kill_openvpn()
                else:
                    connected = kill_openvpn('-9') or True

            if is_connected():
                return 'Could not terminate OpenVPN process.'

        manage_dns("restore")
        manage_ipv6("restore")
        manage_killswitch("restore")
        return 'Disconnected.'

    @staticmethod
    def connect_fastest():
        fastest()
