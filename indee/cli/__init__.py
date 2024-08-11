from indee.types.configs import Configs
from indee.engine import ffprobe
from indee import logger

class IndeeCli:
    def __init__(self, config: Configs, args: dict) -> None:
        self.config = config
        self.args = args
    
    def run(self) -> None:
        logger.info(f"provided input file: {self.args.input}")
        ffprobe_instance = ffprobe.Ffrobe(self.args.input)
        
        metadata = ffprobe_instance.readable_metadata()
        logger.info(f'input file metadata: {metadata}')