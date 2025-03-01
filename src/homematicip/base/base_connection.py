class HmipConnectionError(Exception):
    pass


class HmipWrongHttpStatusError(HmipConnectionError):
    def __init__(self, status_code=None):
        self.status_code = status_code

    def __str__(self):
        return f"HmipWrongHttpStatusError({self.status_code})"


class HmipServerCloseError(HmipConnectionError):
    pass


class HmipThrottlingError(HmipConnectionError):
    pass
