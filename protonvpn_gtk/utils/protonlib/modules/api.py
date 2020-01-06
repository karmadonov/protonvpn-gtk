import json
import urllib.request


class ProtonAPI:
    api_url = "https://api.protonmail.ch"
    api_version = '3'

    def call(self, endpoint: str) -> dict:
        headers = {
            "x-pm-appversion": "Other",
            "x-pm-apiversion": self.api_version,
            "Accept": "application/vnd.protonmail.v1+json"
        }
        url = f'{self.api_url}/{endpoint}'

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = response.read()
        return json.loads(data)

    def get_connection_info(self) -> dict:
        """ Get information about connection.
            Response example:
                {'Code': 1000,
                 'IP': '95.67.56.103',
                 'Lat': 50.4333,
                 'Long': 30.5167,
                 'Country': 'UA',
                 'ISP': 'Cosmonova LLC'}
        """
        return self.call('vpn/location')

    def get_servers(self) -> list:
        """ Get list of VPN servers."""
        return self.call('vpn/logicals')['LogicalServers']
