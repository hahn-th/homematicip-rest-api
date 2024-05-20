class HmipConnectionError(Exception):
    pass


class HmipServerCloseError(HmipConnectionError):
    pass


class HmipThrottlingError(HmipConnectionError):
    pass
