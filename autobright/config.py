import pathlib
from typing import List

import appdirs
import tomli

from autobright.ddccontrol import DDCControl


class TomlConfig:
    def __init__(self):
        config_dir = pathlib.Path(
            appdirs.user_config_dir("autobright", "Martin Ueding")
        )
        config_path = config_dir / "config.toml"
        with open(config_path, "rb") as f:
            self.config = tomli.load(f)

    def make_ddccontrol(self) -> List[DDCControl]:
        return [DDCControl(device) for device in self.config["ddccontrol"]["devices"]]
