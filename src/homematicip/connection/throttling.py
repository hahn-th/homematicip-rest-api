"""Remembers when the cloud last throttled this process.

The cloud throttles by public IP, so one 429 from any connection or access point means every call from
this process is blocked for a while. The app shows the block for at least 15 minutes and no response has
carried a Retry-After header so far, so the cooldown is a fixed guess.
"""

import time

THROTTLE_COOLDOWN = 900.0

_throttled_at: float | None = None


def record_throttled() -> None:
    """Call when the cloud answered with a 429."""
    global _throttled_at
    _throttled_at = time.monotonic()


def throttle_cooldown_remaining() -> float:
    """Seconds until a call to the cloud is worth trying again, 0 when it is not throttled."""
    if _throttled_at is None:
        return 0.0
    return max(0.0, THROTTLE_COOLDOWN - (time.monotonic() - _throttled_at))


def clear_throttled() -> None:
    """Forget the last 429, for tests and for clients that know the block is over."""
    global _throttled_at
    _throttled_at = None
