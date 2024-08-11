from loguru import logger

from indee.settings.config import load_config
from indee.types.configs import Configs as ConfigType
from dataclasses import dataclass

# dataclass to store config values, with ConfigType as type
@dataclass
class Config:
    config: ConfigType # ConfigType as type

# load config from yaml file, and store it in Config object
configs = Config(config=load_config("config.yaml"))

# set logger, with log level from config, and the stdout sink
logger.remove()
logger.add(sink=print, level=configs.config.log.level)


logger.info("config loaded successfully") # log info message
logger.info(f"set log level to {configs.config.log.level}") # log debug message