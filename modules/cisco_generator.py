"""Generate a small, validated Cisco IOS interface configuration."""

import ipaddress
import re


def generate_interface_config(
    hostname: str,
    interface: str,
    ip_address: str,
    subnet_mask: str,
    description: str = "",
) -> str:
    """Generate IOS commands for one IPv4 interface."""
    hostname = hostname.strip()
    interface = interface.strip()
    description = description.strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,62}", hostname):
        raise ValueError("Hostname must be 1–63 letters, digits, or hyphens.")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9/.-]{0,31}", interface):
        raise ValueError("Enter a valid interface name, such as GigabitEthernet0/0.")
    if "\n" in description or "\r" in description:
        raise ValueError("Description must fit on a single line.")
    try:
        address = ipaddress.IPv4Address(ip_address.strip())
        network = ipaddress.IPv4Network(
            (address, subnet_mask.strip()), strict=False
        )
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as exc:
        raise ValueError("Enter a valid IPv4 address and contiguous subnet mask.") from exc

    lines = [
        "configure terminal",
        f"hostname {hostname}",
        f"interface {interface}",
    ]
    if description:
        lines.append(f"description {description}")
    lines.extend(
        [
            f"ip address {address} {network.netmask}",
            "no shutdown",
            "end",
            "write memory",
        ]
    )
    return "\n".join(lines)
