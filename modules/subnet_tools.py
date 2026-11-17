"""IPv4 subnet-mask validation and address calculations."""

import ipaddress


def analyze_subnet(ip_address: str, subnet_mask: str) -> dict[str, object]:
    """Return subnet details for an IPv4 address and contiguous subnet mask."""
    try:
        address = ipaddress.IPv4Address(ip_address.strip())
        network = ipaddress.IPv4Network(
            (address, subnet_mask.strip()), strict=False
        )
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as exc:
        raise ValueError("Enter a valid IPv4 address and contiguous subnet mask.") from exc

    prefix = network.prefixlen
    if prefix <= 30:
        first_usable = str(network.network_address + 1)
        last_usable = str(network.broadcast_address - 1)
        usable_hosts = network.num_addresses - 2
    elif prefix == 31:
        first_usable = str(network.network_address)
        last_usable = str(network.broadcast_address)
        usable_hosts = 2
    else:
        first_usable = last_usable = str(network.network_address)
        usable_hosts = 1

    return {
        "network": str(network),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "prefix_length": prefix,
        "total_addresses": network.num_addresses,
        "usable_hosts": usable_hosts,
        "first_usable": first_usable,
        "last_usable": last_usable,
    }
