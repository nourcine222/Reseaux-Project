"""UTF-8 Base64 and hexadecimal conversion helpers."""

import base64
import binascii
import re


def encode_base64(text: str) -> str:
    """Encode UTF-8 text as Base64."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_base64(value: str) -> str:
    """Decode Base64 into UTF-8 text."""
    try:
        decoded = base64.b64decode(value.strip(), validate=True)
        return decoded.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Input must be valid Base64 containing UTF-8 text.") from exc


def encode_hex(text: str) -> str:
    """Encode UTF-8 text as lowercase hexadecimal."""
    return text.encode("utf-8").hex()


def decode_hex(value: str) -> str:
    """Decode hexadecimal bytes as UTF-8 text."""
    compact = re.sub(r"[\s:-]", "", value)
    if not compact or len(compact) % 2 or not re.fullmatch(r"[0-9A-Fa-f]+", compact):
        raise ValueError("Enter an even number of hexadecimal digits.")
    try:
        return bytes.fromhex(compact).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Hexadecimal data must represent UTF-8 text.") from exc
