import os
from dataclasses import dataclass
from typing import List

@dataclass
class Log:
    """
    Log:
        dataclass to store log related configs
    """
    enable: bool = True
    level: str = "INFO"
    
    # allowed log levels
    allowd_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    def __post_init__(self):
        # check if log level is valid
        if self.level not in self.allowd_levels:
            raise ValueError(f"invalid log level provided, allowed levels are {self.allowd_levels}")

@dataclass
class Server:
    """
    Server:
        dataclass to store server related configs
    """
    enable: bool
    port: int
    metrics: dict
    
    def __post_init__(self):
        # check if port is provided
        if self.enable and not self.port:
            raise ValueError("port must be provided")
        # check if port is valid
        if self.enable and self.port <= 0 or self.port > 65535:
            raise ValueError("invalid port provided")
        # check if metrics is provided
        if self.enable and not self.metrics:
            raise ValueError("metrics must be provided")
 
@dataclass
class Database:
    """
    Database:
        dataclass to store database related configs
    """
    enable: bool
    service: str

    available_services = ["sqlite"]

    def __post_init__(self):
        # check if service is provided
        self.service = self.service.lower()
        if self.enable and self.service not in self.available_services:
            raise ValueError(f"invalid database service provided, available services are {self.available_services}")

@dataclass
class BasicConfig:
    """
    BasicConfig:
        dataclass to store basic configs
    """
    db: Database
    server: Server

@dataclass
class Cache:
    """
    Cache:
        dataclass to store cache related configs
    """
    dirname: str

    prefix: str = "%"
    
    funcs = {
        "WORDIR": os.getcwd,
        "DATE": lambda: datetime.now().strftime("%Y-%m-%d")
    }
    
    def __post_init__(self):
        # check if cache dir is provided
        if not self.dirname:
            self.dirname = "%WORDIR/.cache/%DATE/" # set default cache dir
        
    def get_cache_dir(self):
        """
        get_cache_dir:
            get cache dir with variables replaced
        """
        variables: List[str] = [ "WORDIR", "DATE" ]
        cache_dir = self.dirname # set cache dir
        for var in variables:
            if self.prefix + var in cache_dir:
                cache_dir = cache_dir.replace(f"{self.prefix}{var}", self.funcs[var]()) # replace variable with value, if found
        return cache_dir

@dataclass
class Configs:
    """
    Configs:
        dataclass to store config values
    """
    version: str
    log: Log
    configs: BasicConfig
    cache: Cache