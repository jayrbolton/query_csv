
class QueryCSVError(RuntimeError):
    """Simple base class for library errors"""

    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidFileError(QueryCSVError):
    """Invalid input file; nonexistent or incorrect extension"""
    pass
