"""IPv6 address formatting helpers."""

import ipaddress


def compress_ipv6(address: str) -> str:
    """Validate an IPv6 address and return its compressed representation."""
    try:
        return str(ipaddress.IPv6Address(address.strip()))
    except ipaddress.AddressValueError as exc:
        raise ValueError("Enter a valid IPv6 address.") from exc


def expand_ipv6(address: str) -> str:
    """Validate an IPv6 address and return all eight groups."""
    try:
        return ipaddress.IPv6Address(address.strip()).exploded
    except ipaddress.AddressValueError as exc:
        raise ValueError("Enter a valid IPv6 address.") from exc
