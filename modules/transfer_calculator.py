"""File-transfer duration calculations."""

import math

SIZE_UNITS = {"B": 1, "KB": 1_000, "MB": 1_000_000, "GB": 1_000_000_000}
RATE_UNITS = {"Kbps": 1_000, "Mbps": 1_000_000, "Gbps": 1_000_000_000}


def calculate_transfer_seconds(
    size: float, size_unit: str, rate: float, rate_unit: str
) -> float:
    """Calculate ideal transfer time in seconds using decimal SI units."""
    if size_unit not in SIZE_UNITS or rate_unit not in RATE_UNITS:
        raise ValueError("Choose a supported size unit and network speed unit.")
    if not math.isfinite(size) or not math.isfinite(rate) or size <= 0 or rate <= 0:
        raise ValueError("File size and network speed must be greater than zero.")
    return size * SIZE_UNITS[size_unit] * 8 / (rate * RATE_UNITS[rate_unit])


def format_duration(seconds: float) -> str:
    """Format non-negative seconds as a readable duration."""
    if seconds < 0:
        raise ValueError("Duration cannot be negative.")
    whole_seconds = round(seconds)
    hours, remainder = divmod(whole_seconds, 3600)
    minutes, remaining_seconds = divmod(remainder, 60)
    if hours:
        return f"{hours} h {minutes} min {remaining_seconds} s"
    if minutes:
        return f"{minutes} min {remaining_seconds} s"
    if whole_seconds:
        return f"{whole_seconds} s"
    return f"{seconds:.2f} s"
