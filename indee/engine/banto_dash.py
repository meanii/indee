import subprocess

from typing import List
from pathlib import Path
from indee import logger
from indee import configs
from indee.utils.exec import exec_command


class BantoDash:
    """
    BantoDash:
        represents wrapper for BantoDash,
        contain some usefull methods
    """
    def __init__(
        self,
        name: str,
        banto_dir: str, 
        inputs: list[str], 
        workdir: str,
        is_hdr: bool = False
    ) -> None:
        self.banto_dir = banto_dir
        self.inputs = inputs
        self.is_hdr = is_hdr
        
        self.mp4fragment = str(Path(self.banto_dir) / "bin" / "mp4fragment")
        self.mp4dash = str(Path(self.banto_dir) / "bin" / "mp4dash")
        
        self.name = name
        self.workdir = workdir
        self.banto_dir = str(Path.resolve(Path(self.banto_dir))) # resolve banto_dir path, to get absolute path
        self.workdir = str(Path.resolve(Path(self.workdir))) # resolve workdir path, to get absolute path
        
        if (not isinstance(banto_dir, str)):
            logger.error(f"BantoDash: {banto_dir} not found")
            raise TypeError("banto_dir must be str")
        
        if not self.__banto_dir_verification():
            logger.error(f"BantoDash: {banto_dir} not found")
            raise FileNotFoundError(f"{banto_dir} not found")
        
        if not isinstance(inputs, (list, str)):
            logger.error(f"BantoDash: {inputs} not found")
            raise TypeError("inputs must be list of str")
        
        if not isinstance(workdir, str):
            logger.error(f"BantoDash: {workdir} not found")
            raise TypeError("workdir must be str")
        
        if not Path(workdir).exists():
            logger.error(f"BantoDash: {workdir} not found")
            raise FileNotFoundError(f"{workdir} not found")
    
    def package(self) -> str:
        """
        package:
            package the input files
            into banto format
            example: mp4dash --mpd-name myvideo.mpd myvideo_1920x1080_frag.mp4 \
                        myvideo_1280x720_frag.mp4 \
                        myvideo_640x360_frag.mp4 myvideo_320x180_frag.mp4
        """
        fragments_record = []
        for inputfile in self.inputs:
            outputfile = str(Path(self.workdir) / "fragments" / Path(inputfile).name)
            self.__make_sure_dir_exists(outputfile)
            self.__fragment(
                input_file=inputfile,
                output_file=outputfile,
                segment_length=configs.config.banto.get('fragment')
            )
            logger.info(f'BantoDash: fragmented {inputfile}')
            fragments_record.append(outputfile)
        
        hdr_folder = self.is_hdr and "hdr" or "sdr"
        manifest = str(Path(self.workdir) / "dash" / hdr_folder / f"{self.name}.mpd")
        self.__make_sure_dir_exists(manifest)
        
        command = f"{self.mp4dash} -f --mpd-name {str(Path(manifest).name)} --output-dir={str(Path(manifest).parent)} {' '.join(fragments_record)}"
        logger.info(f"BantoDash: packaging {self.inputs} into {manifest}, CMD: {command}")
        exec_command(command.split())
        logger.info(f"BantoDash: packaged {self.inputs} into {manifest}")
        return manifest
    
    def __fragment(
        self, 
        input_file: str, 
        output_file: str,
        segment_length: int = 8000
    ) -> None:
        """
        __fragment:
            fragment the input files
            into smaller chunks
            example: mp4fragment --fragment-duration 4000 myvideo_1920x1080.mp4 myvideo_1920x1080_fragmented.mp4
        """
        if not isinstance(input_file, str):
            raise TypeError("file must be str")
        
        if not isinstance(output_file, str):
            raise TypeError("output_file must be str")

        if not isinstance(segment_length, int):
            raise TypeError("segment_length must be int")
        
        if not Path(input_file).exists():
            raise FileNotFoundError(f"{input_file} not found")
        
        command = f"{self.mp4fragment} --fragment-duration {segment_length} {input_file} {output_file}"
        logger.info(f"BantoDash: fragmenting {input_file}: {command}")
        exec_command(command.split())
        

    def __banto_dir_verification(self) -> None:
        """
        __banto_dir_verification:
            verify if banto_dir is valid
        """
        list_of_dir_should_exist = ["bin", "lib", "include"]
        for dirname in list_of_dir_should_exist:
            if not Path(str(Path(self.banto_dir) / dirname)).exists():
                logger.error(f"BantoDash: {self.banto_dir / dirname} not found")
                return False
        
        if not Path(self.mp4fragment).exists():
            logger.error(f"BantoDash: {self.mp4fragment} not found")
            return False

        if not Path(self.mp4dash).exists():
            logger.error(f"BantoDash: {self.mp4dash} not found")
            return False
        
        return True
    
    def __make_sure_dir_exists(self, path: str) -> None:
        """
        __make_sure_dir_exists:
            make sure directory exists
        """
        dirname = Path(path).parent
        if not dirname.exists():
            logger.info(f"creating directory: {dirname}")
            dirname.mkdir(parents=True, exist_ok=True)