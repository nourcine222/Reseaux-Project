"""MAC address normalization and display formats."""

import re


def convert_mac_address(address: str) -> dict[str, str]:
    """Return common colon, hyphen, and Cisco dotted MAC address formats."""
    hex_digits = re.sub(r"[:.\-\s]", "", address.strip())
    if not re.fullmatch(r"[0-9A-Fa-f]{12}", hex_digits):
        raise ValueError("Enter a 48-bit MAC address with 12 hexadecimal digits.")
    value = hex_digits.lower()
    return {
        "colon": ":".join(value[index : index + 2] for index in range(0, 12, 2)),
        "hyphen": "-".join(value[index : index + 2] for index in range(0, 12, 2)),
        "cisco": ".".join(value[index : index + 4] for index in range(0, 12, 4)),
        "uppercase": value.upper(),
    }
