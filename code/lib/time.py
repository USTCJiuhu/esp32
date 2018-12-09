from utime import *
from micropython import const
try:
    import struct
except ImportError:
    import ustruct as struct


_prev_ticks_ms = 0
_total_ms = 0

def monotonic():
    """A monotonically increasing time in seconds. No defined start time."""
    # Assumes that monotonic is called more frequently than the wraparound of micropython's
    # utime.ticks_ms()
    global _prev_ticks_ms, _total_ms
    ticks_ms_ = ticks_ms()
    _total_ms += ticks_diff(ticks_ms_, _prev_ticks_ms)
    _prev_ticks_ms = ticks_ms_
    return _total_ms * 0.001
