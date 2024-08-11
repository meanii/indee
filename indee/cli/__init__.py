import time
from pathlib import Path
from indee.types.configs import Configs
from indee.engine.iffmpeg import IndeeFfmpeg
from indee.engine.banto_dash import BantoDash
from indee import logger

class IndeeCli:
    def __init__(self, config: Configs, args: dict) -> None:
        self.config = config
        self.args = args
    
    def run(self) -> None:
        """
        run:
            run the indee, based on the provided args
        """
        logger.info(f"provided input file: {self.args.input}")
        
        iffmpeg_instance = IndeeFfmpeg(self.args.input)
        cache_path = self.config.cache.get_cache_dir()

        hdr_output_files = [];
        sdr_output_files = [];
       
        for resolution in ['360p']:
            output = str(Path(cache_path) / resolution / f"{resolution}.mp4")
            output_files = iffmpeg_instance.transcode(output, resolution, 'h265')
            
            # append the output files to the respective list
            if output_files.get('hdr'):
                logger.info(f"hdr output file: {output_files.get('hdr')}")
                hdr_output_files.append(output_files.get('hdr'))
            if output_files.get('sdr'):
                logger.info(f"sdr output file: {output_files.get('sdr')}")
                sdr_output_files.append(output_files.get('sdr'))
                
        logger.info(f"transcoding completed for {self.args.input}")
        
        # package the transcoded files, into banto format
        if hdr_output_files:
            bando_dash_instance_hdr = BantoDash(
                name="manifest-hdr",
                banto_dir=self.config.banto.get('banto_dir'),
                inputs=hdr_output_files,
                workdir=cache_path,
                is_hdr=True
            )
            logger.info(f"packaging hdr files")
            packed_file_hdr = bando_dash_instance_hdr.package()
            logger.info(f"packaged hdr files")
        
        if sdr_output_files:
            bando_dash_instance_sdr = BantoDash(
                name="manifest-sdr",
                banto_dir=self.config.banto.get('banto_dir'),
                inputs=sdr_output_files,
                workdir=cache_path,
                is_hdr=False
            )
            logger.info(f"packaging sdr files")
            packed_file_sdr = bando_dash_instance_sdr.package()
            logger.info(f"packaged sdr files")
        
        logger.info(f"packaging completed for {self.args.input}")
        print('#'*50)
        print('ffplay', packed_file_hdr)
        print('ffplay', packed_file_sdr)