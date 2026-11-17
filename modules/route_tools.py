"""IPv4 route aggregation helpers."""

import ipaddress
from collections.abc import Iterable


def summarize_routes(routes: Iterable[str]) -> list[str]:
    """Collapse IPv4 networks into the smallest set of covering routes."""
    networks = []
    for route in routes:
        candidate = route.strip()
        if not candidate:
            continue
        if "/" not in candidate:
            raise ValueError(f"Route must include a CIDR prefix: {candidate}")
        try:
            networks.append(ipaddress.IPv4Network(candidate, strict=False))
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as exc:
            raise ValueError(f"Invalid IPv4 route: {candidate}") from exc

    if not networks:
        raise ValueError("Enter at least one IPv4 network in CIDR notation.")

    return [str(network) for network in ipaddress.collapse_addresses(networks)]
