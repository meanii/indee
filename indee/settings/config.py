from yaml import safe_load
from os import path
from dataclasses import dataclass

from indee.types.configs import Configs
from indee.utils.dict_to_dataclasses import dataclass_from_dict

def load_config(config_path: str, key: str = 'indee_video_engine') -> Configs:
    """
    load_config:
        load config from yaml file
    """
    # check if config_path is file
    if not path.isfile(config_path):
        raise FileNotFoundError(f"config file not found: {config_path}")
    
    # read config file
    with open(config_path, "r") as file:
        config = safe_load(file)
        file.close()
    
    if key not in config:
        raise KeyError(f"key: {key} not found in config")
    
    # return config as Configs object
    return dataclass_from_dict(Configs, config[key])