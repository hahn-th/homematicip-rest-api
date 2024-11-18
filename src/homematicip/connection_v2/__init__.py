# Connection constants
ATTR_AUTH_TOKEN: str = "AUTHTOKEN"
ATTR_CLIENT_AUTH: str = "CLIENTAUTH"

THROTTLE_STATUS_CODE: int = 429

# Initial rate limiter settings
RATE_LIMITER_TOKENS: int = 10       # Number of tokens in the bucket
RATE_LIMITER_FILL_RATE: int = 8     # Fill rate of the bucket in tokens per second
