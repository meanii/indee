import ffmpeg

class Ffrobe:
    """
    Ffrobe:
        represents wrapper for ffrobe,
        contain some usefull methods
    """
    inputs: list[str]

    def __init__(self, inputs: list[str]):
        # make sure inputs is list of str
        if not isinstance(inputs, list) or not isinstance(inputs, str):
            raise TypeError("inputs must be list of str, or str")
        
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