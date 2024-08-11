from dataclasses import dataclass

@dataclass
class VideoMetadata:
    """
    VideoMetadat:
        dataclass to store video metadata
    """
    file_path: str
    duration: float
    frame_rate: float
    resolution: tuple
    codec_name: str
    codec_type: str
    bit_rate: int
    size: int
    
    # custom fields, to store additional metadata
    isHDR: bool = False
    isSDR: bool = False