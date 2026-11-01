class HmipConnectionError(Exception):
    """
    Exception raised for errors in the HomematicIP connection.

    :param message: Optional error message
    """
    def __init__(self, message: str | None = None):
        super().__init__(message)
        self.message = message


class HmipServerCloseError(HmipConnectionError):
    pass


class HmipThrottlingError(HmipConnectionError):
    pass


class HmipRefreshBudgetError(HmipConnectionError):
    """Raised when more full state downloads were started within the budget window than a healthy client needs.

    Every throttling incident so far was a reconnect loop downloading the whole home over and over, so the
    download refuses to run instead of letting the cloud block the IP.
    """


class HmipAuthenticationError(HmipConnectionError):
    """Exception raised when the HomematicIP cloud returns an authentication error (HTTP 403)."""
