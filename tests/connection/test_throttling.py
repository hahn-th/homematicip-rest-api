from unittest.mock import patch

from homematicip.connection import throttling


def test_not_throttled_by_default():
    assert throttling.throttle_cooldown_remaining() == 0.0


def test_cooldown_counts_down_from_the_last_429():
    clock = [1000.0]
    with patch("homematicip.connection.throttling.time.monotonic", side_effect=lambda: clock[0]):
        throttling.record_throttled()
        assert throttling.throttle_cooldown_remaining() == throttling.THROTTLE_COOLDOWN
        clock[0] += 100
        assert throttling.throttle_cooldown_remaining() == throttling.THROTTLE_COOLDOWN - 100
        clock[0] += throttling.THROTTLE_COOLDOWN
        assert throttling.throttle_cooldown_remaining() == 0.0


def test_clear_forgets_the_last_429():
    throttling.record_throttled()
    throttling.clear_throttled()
    assert throttling.throttle_cooldown_remaining() == 0.0
