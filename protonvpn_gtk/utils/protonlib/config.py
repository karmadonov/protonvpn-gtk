from configparser import ConfigParser

from .consts import (
    CONFIG_FILE,
    CONFIG_DIR,
    USER_SETTINGS,
    METADATA_SETTINGS
)
from .errors import ProtonVPNException


class Settings:

    def __init__(self, config_dir=CONFIG_DIR, config_file=CONFIG_FILE):
        self.config_dir = config_dir
        self.config_file = config_file
        self.user = {}
        self.metadata = {}

    def init(self):
        """ Create initial configs """

    def load(self) -> None:
        if not self.config_file.exists():
            raise ProtonVPNException(f'File {self.config_file} do not exists')
        config = ConfigParser()
        config.read(self.config_file)

        self.user = {}
        for key, value in config.items('USER'):
            self.user[key] = USER_SETTINGS.get(key, str)(value)

        self.metadata = {}
        for key, value in config.items('metadata'):
            self.metadata[key] = METADATA_SETTINGS.get(key, str)(value)

    def save(self) -> None:
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        config = ConfigParser()
        config['USER'] = {k: str(v) for k, v in self.user.items()}
        config['metadata'] = {k: str(v) for k, v in self.metadata.items()}
        with self.config_file.open('w') as config_file:
            config.write(config_file)
