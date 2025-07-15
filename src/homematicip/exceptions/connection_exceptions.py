class HmipConnectionError(Exception):
    """
    Exception raised for errors in the HomematicIP connection.

    :param message: Optional error message
    """
    def __init__(self, message: str = None):
        super().__init__(message)
        self.message = message


class HmipServerCloseError(HmipConnectionError):
    pass


class HmipThrottlingError(HmipConnectionError):
    pass
