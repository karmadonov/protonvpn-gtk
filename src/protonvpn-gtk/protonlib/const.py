import os

from enum import Enum
from pathlib import Path


USER = os.environ.get("SUDO_USER", os.environ["USER"])
HOME_DIR = Path(f'~{USER}').expanduser()
CONFIG_DIR = HOME_DIR.joinpath('.proton')
USER_CONFIG_FILE = CONFIG_DIR.joinpath("user.json")
METADATA_CONFIG_FILE = CONFIG_DIR.joinpath("metadata.json")


class TIER(Enum):
    FREE = 1
    BASIC = 2
    PLUS = 3
    VISIONARY = 4


class PROTOCOL(Enum):
    UDP = 1
    TCP = 2
