from .config import Config
from .consts import (
    USER_CONFIG_FILE,
    METADATA_CONFIG_FILE,
    PROTOCOL,
    TIER
)
from .system import is_connected


class ProtonVPN:

    def __init__(self):
        self.user = Config(USER_CONFIG_FILE)
        self.metadata = Config(METADATA_CONFIG_FILE)

    def init(self,
             username: str,
             password: str,
             tier: TIER = TIER.FREE,
             protocol: PROTOCOL = PROTOCOL.UDP,
             dns_leak_protection: bool = True,
             custom_dns: str = '',
             killswitch: bool = False) -> None:
        """ Create settings file for a new user """
        user_data = dict(
            username=username,
            password=password,
            tier=tier,
            protocol=protocol,
            dns_leak_protection=dns_leak_protection,
            custom_dns=custom_dns,
            killswitch=killswitch
        )
        self.user.update(user_data)

    def is_connected(self) -> bool:
        """ Return connection status """
        return self.is_connected()
