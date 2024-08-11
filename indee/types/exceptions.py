class BinNotFoundOrInvalid(Exception):
    """Raise when bin not found, or provided invalid"""

    def __init__(self, bin: str, message: str = "provided bin not found or invalid"):
        self.path = bin
        self.message = message
        super().__init__(self.message)

class WrongInputFile(Exception):
    """Raise when wrong input provided"""

    def __init__(self, inputs: list[str], message: str = "wrong input provided"):
        self.inputs = inputs
        self.message = message
        super().__init__(self.message)

class WrongInputFile(Exception):
    """Raise when wrong input provided"""

    def __init__(self, inputs: list[str], message: str = "wrong input provided"):
        self.inputs = inputs
        self.message = message
        super().__init__(self.message)