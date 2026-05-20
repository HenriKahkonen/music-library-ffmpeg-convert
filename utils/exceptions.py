class InvalidFileFormatException(Exception):
    """Exception thrown if the user specified file format is not valid

        Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidDirectoryException(Exception):
    """Exception thrown if the user specified directory path is not valid in some way

        Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidFileFormatException(Exception):
    """Exception thrown if the user specified file format is not valid

        Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

