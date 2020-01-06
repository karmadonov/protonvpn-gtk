from collections import defaultdict

from .api import ProtonAPI
from .consts import COUNTRY_CODES


class Servers:

    def __init__(self, user_tier: int) -> None:
        self.user_tier = user_tier
        self.servers = {}
        self.countries = {}

    @staticmethod
    def _load(user_tier: int) -> (dict, dict):
        api = ProtonAPI()
        servers_data = api.get_servers()

        servers = {}
        countries = defaultdict(lambda: {
            'features': set(),
            'name': None,
            'servers': list()
        })
        for server in servers_data:
            if server["Tier"] > user_tier or server["Status"] != 1:
                continue
            servers[server['ID']] = server

            country_code = server["ExitCountry"]
            country = countries[country_code]
            country['name'] = COUNTRY_CODES.get(country_code, None)
            country['features'].add(int(server['Features']))
            country['servers'].append(server['ID'])
        return servers, countries

    def update(self):
        self.servers, self.countries = self._load(self.user_tier)

    def get_coutries(self) -> dict:
        if not self.countries:
            self.update()
        return self.countries

    def get_servers_by_country(self, country_code: str) -> dict:
        if not self.countries:
            self.update()

        servers = {}
        for server_id in self.countries[country_code]['servers']:
            servers[server_id] = self.servers.get(server_id)
        return servers

    def get_server(self, server_id: str) -> dict:
        return self.servers.get(server_id)
