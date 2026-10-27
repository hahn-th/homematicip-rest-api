import ssl

# Connection constants
ATTR_AUTH_TOKEN: str = "AUTHTOKEN"
ATTR_CLIENT_AUTH: str = "CLIENTAUTH"
ATTR_ACCESSPOINT_ID: str = "ACCESSPOINT-ID"

THROTTLE_STATUS_CODE: int = 429

# Initial rate limiter settings
RATE_LIMITER_TOKENS: int = 10  # Number of tokens in the bucket
RATE_LIMITER_FILL_RATE: int = 8  # Fill rate of the bucket in tokens per second


def get_ssl_verify(
    enforce_ssl: bool, ssl_ctx: ssl.SSLContext | str | bool | None
) -> ssl.SSLContext | bool:
    """aiohttp rejects a CA file path and httpx deprecated it, so it becomes a context."""
    if isinstance(ssl_ctx, str):
        return ssl.create_default_context(cafile=ssl_ctx)
    if ssl_ctx is not None:
        return ssl_ctx
    return enforce_ssl
