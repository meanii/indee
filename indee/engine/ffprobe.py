import ffmpeg
from typing import List
from indee.types.video_metadata import VideoMetadata

class Ffrobe:
    """
    Ffrobe:
        represents wrapper for ffrobe,
        contain some usefull methods
    """
    inputs: List[str]

    def __init__(self, inputs: list[str]):
        # make sure inputs is list of str
        if not isinstance(inputs, (list, str)):
            raise TypeError("inputs must be list of str")
        
        # set inputs, if inputs is str, convert to list
        if isinstance(inputs, list):
            self.inputs = inputs
        
        if isinstance(inputs, str):
            self.inputs = [inputs]
        
        self.bin = "ffprobe"
    
    def get_metadata(self):
        """
        get_metadata:
            get metadata from input file
        """
        try:
            metadata = {}
            for input in self.inputs:
                # get metadata from input
                metadata = ffmpeg.probe(input)
                metadata[input] = metadata # store metadata, with input as key
            return metadata
        except ffmpeg.Error as e:
            # raise error if something wrong
            raise e
    
    def is_hdr(self, metadata: dict):
        """
        is_hdr:
            check if input file is hdr
            check if metadata has color_space, and color_space is bt2020nc
            return True if both condition met, otherwise False
            refer to https://www.radiantmediaplayer.com/blog/how-to-tell-if-my-video-file-is-hdr.html
            for more information, how to check if video is hdr
        """
        try:
            # codec_name: HDR video content generally uses modern video codecs (H.265/HEVC, AV1 or Apple ProRes)
            # width/height: typical video resolutions for HDR video content are 1920×1080 ("Full HD"), 3840×2160 ("4K UHD") and 7680×4320 ("8K UHD").
            # pix_fmt: pixel format - in our example this is yuv420p10le - this means YUV color model with 4:2:0 chroma subsampling (this is the most common chroma subsampling
            # found in online video but note that studio master files can be encoded with 4:2:2 or 4:4:4 chroma subsampling) and planar 10 bits color depth (the "p10" part)
            # color_primaries: for HDR video this will be bt2020 (if you see bt709 then this is SDR video content)
            
            return all([metadata["streams"][0]["codec_name"] in ["hevc", "av1", "prores"],
                        metadata["streams"][0]["width"] in [1920, 3840, 7680],
                        metadata["streams"][0]["height"] in [1080, 2160, 4320],
                        metadata["streams"][0]["pix_fmt"] == "yuv420p10le",
                        metadata["streams"][0]["color_primaries"] == "bt2020"])
        except ffmpeg.Error as e:
            # raise error if something wrong
            raise e
    
    def readable_metadata(self) -> VideoMetadata:
        """
        readable_metadata:
            convert metadata to readable format
        """
        try:
            metadata = self.get_metadata()
            # convert metadata to readable format
            return VideoMetadata(
                file_path=metadata["format"]["filename"],
                duration=metadata["format"]["duration"],
                frame_rate=metadata["streams"][0]["r_frame_rate"],
                resolution=(metadata["streams"][0]["width"], metadata["streams"][0]["height"]),
                codec_name=metadata["streams"][0]["codec_name"],
                codec_type=metadata["streams"][0]["codec_type"],
                bit_rate=metadata["streams"][0]["bit_rate"],
                size=metadata["format"]["size"],
                is_hdr=self.is_hdr(metadata),
                is_sdr=not self.is_hdr(metadata)
            )
            
        except ffmpeg.Error as e:
            # raise error if something wrong
            raise e