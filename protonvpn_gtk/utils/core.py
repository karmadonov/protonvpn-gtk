import configparser
import datetime
import os
import subprocess
import time

from protonvpn_cli.constants import CONFIG_FILE, CONFIG_DIR
from protonvpn_cli.utils import (
    get_ip_info,
    get_country_name,
    get_servers,
    get_server_value,
    pull_server_data,
)


class ProtonVPN:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        self.config = {s: dict(config.items(s)) for s in config.sections()}

    @property
    def is_connected(self) -> bool:
        """ Check if VPN is connected."""
        openvpn_pids = subprocess \
            .run(["pgrep", "openvpn"], stdout=subprocess.PIPE) \
            .stdout.decode("utf-8").split()
        return bool(openvpn_pids)

    @property
    def is_killswitch_active(self) -> bool:
        """ Check if Kill Switch is active """
        return os.path.isfile(os.path.join(CONFIG_DIR, "iptables.backup"))

    @staticmethod
    def is_server_reachable(server: str) -> bool:
        """ Check if the VPN Server is reachable """
        ping = subprocess.run(["ping", "-c", "1", server],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        return ping.returncode == 0

    def _check_configs(self) -> bool:
        if 'USER' not in self.config:
            return False

        if self.config['USER'].get("initialized", None) != '1':
            return False

        required_props = {"username", "tier", "default_protocol",
                          "dns_leak_protection", "custom_dns"}
        return not bool(required_props - self.config['USER'].keys())

    def status(self) -> str:
        """ Return the current VPN status.

            Showing connection status (connected/disconnected),
            current IP, server name, country, server load
        """
        if not self._check_configs():
            return 'Settings problem. Please run "protonvpn init".'

        if not self.is_connected:
            msgs = ['Not connected']
            if self.is_killswitch_active:
                msgs.append('Kill Switch is currently active.')
            ip, isp = get_ip_info()
            msgs.extend((f'IP: {ip}', f'ISP: {isp}'))
            return '\n'.join(msgs)

        pull_server_data()

        metadata = self.config.get('metadata', {})
        connected_server = metadata.get("connected_server", None)
        connected_protocol = metadata.get("connected_proto", None)
        dns_server = metadata.get("dns_server", None)
        if not metadata or \
                not all((connected_server, connected_protocol, dns_server)):
            return 'Please connect with "protonvpn connect" first.'

        if not self.is_server_reachable(dns_server):
            msgs = ('Could not reach VPN server',
                    'You may want to reconnect with "protonvpn reconnect"')
            return '\n'.join(msgs)

        servers = get_servers()
        subs = [s["Servers"] for s in servers if s["Name"] == connected_server][0]
        server_ips = [subserver["ExitIP"] for subserver in subs]

        ip, isp = get_ip_info()

        if ip not in server_ips:
            msgs = ("Your IP was not found in last Servers IPs",
                    "Maybe you're not connected to a ProtonVPN Server")
            return '\n'.join(msgs)

        all_features = {0: "Normal", 1: "Secure-Core", 2: "Tor", 4: "P2P"}

        country_code = get_server_value(connected_server, "ExitCountry", servers)
        country = get_country_name(country_code)
        city = get_server_value(connected_server, "City", servers)
        load = get_server_value(connected_server, "Load", servers)
        feature = get_server_value(connected_server, "Features", servers)
        last_connection = metadata.get("connected_time")
        connection_time = time.time() - int(last_connection)

        killswitch_status = "Enabled" if self.is_killswitch_active else "Disabled"
        connection_time = str(datetime.timedelta(
            seconds=connection_time)).split(".")[0]

        msgs = (
            "Status: Connected",
            f"Time: {connection_time}",
            f"IP: {ip}",
            f"Server: {connected_server}",
            f"Features: {all_features[feature]}",
            f"Protocol: {connected_protocol.upper()}",
            f"Kill Switch: {killswitch_status}",
            f"Country: {country}",
            f"City: {city}",
            f"Load: {load}",
        )
        return '\n'.join(msgs)
