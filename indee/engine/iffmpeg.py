import ffmpeg
from os import path, makedirs
from pathlib import Path
from indee import logger
from indee.engine import ffprobe
from indee.types.video_metadata import VideoMetadata


class IndeeFfmpeg:
    """FFmpeg class to handle FFmpeg commands.
    """
    def __init__(self, input: str):
        self.input = input
        
        try:
            # Get video metadata
            ffprobe_instance = ffprobe.Ffrobe(input)
            self.metadata: VideoMetadata = ffprobe_instance.readable_metadata()
        except Exception as e:
            logger.error(f"Failed to get metadata for {input}")
            raise e
        
        # check if input is valid
        if not path.isfile(input):
            raise WrongInputFile(input)
    
    def transcode(self, output: str, resolution: str = '1080p', codec: str = 'h265') -> dict:
        """
        Transcode the video file to different resolution
        """
        # Check if resolution is valid
        if resolution not in ['360p', '480p', '720p', '1080p']:
            raise ValueError(f"Provided resolution: {resolution} not valid")
        
        # Check if codec is valid
        if codec not in ['h265', 'h264']:
            raise ValueError(f"Provided codec: {codec} not valid")
        
        # Map resolution strings to numeric values
        resolution_map = {
            '360p': 360,
            '480p': 480,
            '720p': 720,
            '1080p': 1080
        }
        
        # codec maps to FFmpeg codec
        codec_map = {
            'h265': 'libx265',
            'h264': 'libx264'
        }
        
        # Get height from resolution_map
        height = resolution_map[resolution]
        codeclib = codec_map[codec]
        
        # Make sure output directory exists
        self._make_sure_dir_exists(output)
        
        # output file
        output_files = {
            "hdr": None,
            "sdr": None
        }
        
        # Create output files for both HDR and SDR if input is HDR
        if self.metadata.is_hdr:
            output_files['hdr'] = self._transcode_with_variant(output, height, codeclib, hdr=True)
            output_files['sdr'] = self._transcode_with_variant(output, height, codeclib, hdr=False)
        else:
            output_files['sdr'] = self._transcode_with_variant(output, height, codeclib, hdr=False)
        
        return output_files
        
    
    def _transcode_with_variant(self, output: str, height: int, codec: str, hdr: bool = False) -> str:
        """
        Helper function to transcode with or without HDR.
        """
        # Determine the suffix and circle color based on HDR flag
        variant_suffix = '_hdr' if hdr else '_sdr'
        circle_color = 'green@0.5' if hdr else 'white@0.5'
        output_file = f"{output.replace('.mp4', f'{variant_suffix}.mp4')}"

        # Construct FFmpeg arguments
        ffmpeg_args = {
            'c:v': codec, # video codec, h265 or h264
            'vf': f'scale=-2:{height}', # video filter, scale to height, keep aspect ratio
            'aspect': '16:9', # aspect ratio, 16:9
            'c:a': 'copy' # copy audio codec
        }

        # Apply HDR-specific adjustments
        if hdr:
            ffmpeg_args['vf'] += ',zscale=t=linear:npl=1000'  # HDR tone mapping
            circle_filter = f"drawbox=x=iw-({height*0.07}):y=0:w={height*0.14}:h={height*0.14}:color={circle_color}:t=fill"
            ffmpeg_args['vf'] += f',{circle_filter}'
            logger.info(f"Transcoding HDR variant for {self.input}")
        else:
            # Apply SDR-specific adjustments
            ffmpeg_args['vf'] += (
                ',zscale=t=linear:npl=1000'  # HDR tone mapping
                ',colorspace=all=bt709:trc=bt709:primaries=bt709'  # SDR conversion
            )
            circle_filter = f"drawbox=x=iw-({height*0.05}):y=ih-({height*0.05}):w={height*0.1}:h={height*0.1}:color={circle_color}:t=fill"
            ffmpeg_args['vf'] += f',{circle_filter}'
            logger.info(f"Transcoding SDR variant for {self.input}")

        # Run FFmpeg command
        logger.info(f"Transcoding {self.input} to {output_file}")
        ffmpeg.input(self.input).output(output_file, **ffmpeg_args).run()
        return output_file

        
    def _make_sure_dir_exists(self, path: str):
        """
        Make sure directory exists
        """
        directory = str(Path(path).parent)
        if not Path(directory).exists():
            makedirs(directory) # create directory if not exists