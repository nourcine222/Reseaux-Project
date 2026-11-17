import unittest
from unittest.mock import patch

from modules.cisco_generator import generate_interface_config
from modules.encoding_tools import (
    decode_base64,
    decode_hex,
    encode_base64,
    encode_hex,
)
from modules.ipv6_tools import compress_ipv6, expand_ipv6
from modules.mac_converter import convert_mac_address
from modules.route_tools import summarize_routes
from modules.socket_tester import test_tcp_connection
from modules.subnet_tools import analyze_subnet
from modules.transfer_calculator import calculate_transfer_seconds, format_duration


class NetworkingToolsTests(unittest.TestCase):
    def test_ipv6_round_trip_formats(self):
        address = "2001:0db8:0000:0000:0000:ff00:0042:8329"
        self.assertEqual(compress_ipv6(address), "2001:db8::ff00:42:8329")
        self.assertEqual(
            expand_ipv6(compress_ipv6(address)),
            "2001:0db8:0000:0000:0000:ff00:0042:8329",
        )
        with self.assertRaises(ValueError):
            compress_ipv6("not IPv6")

    def test_subnet_calculations_and_invalid_mask(self):
        result = analyze_subnet("192.168.1.25", "255.255.255.0")
        self.assertEqual(result["network"], "192.168.1.0/24")
        self.assertEqual(result["broadcast_address"], "192.168.1.255")
        self.assertEqual(result["usable_hosts"], 254)
        with self.assertRaises(ValueError):
            analyze_subnet("192.168.1.25", "255.0.255.0")

    def test_route_summarization(self):
        self.assertEqual(
            summarize_routes(["192.168.0.0/24", "192.168.1.0/24"]),
            ["192.168.0.0/23"],
        )
        with self.assertRaises(ValueError):
            summarize_routes(["192.168.1.1"])

    def test_socket_tester_validates_without_connecting(self):
        with patch("modules.socket_tester.socket.create_connection") as connect:
            with self.assertRaises(ValueError):
                test_tcp_connection("", 443)
            with self.assertRaises(ValueError):
                test_tcp_connection("127.0.0.1", 65536)
            connect.assert_not_called()

    def test_transfer_time_units_and_formatting(self):
        seconds = calculate_transfer_seconds(100, "MB", 100, "Mbps")
        self.assertEqual(seconds, 8.0)
        self.assertEqual(format_duration(seconds), "8 s")
        with self.assertRaises(ValueError):
            calculate_transfer_seconds(1, "MB", 0, "Mbps")

    def test_cisco_configuration_and_input_validation(self):
        config = generate_interface_config(
            "R1", "GigabitEthernet0/0", "192.168.1.1", "255.255.255.0", "LAN"
        )
        self.assertIn("ip address 192.168.1.1 255.255.255.0", config)
        self.assertIn("description LAN", config)
        with self.assertRaises(ValueError):
            generate_interface_config("R1\nend", "Gi0/0", "192.0.2.1", "255.255.255.0")

    def test_mac_formats(self):
        converted = convert_mac_address("00:1A:2B:3C:4D:5E")
        self.assertEqual(converted["hyphen"], "00-1a-2b-3c-4d-5e")
        self.assertEqual(converted["cisco"], "001a.2b3c.4d5e")
        with self.assertRaises(ValueError):
            convert_mac_address("00:1A:2B")

    def test_utf8_base64_and_hex_round_trip(self):
        text = "NetTools café"
        self.assertEqual(decode_base64(encode_base64(text)), text)
        self.assertEqual(decode_hex(encode_hex(text)), text)
        with self.assertRaises(ValueError):
            decode_base64("%%%")
        with self.assertRaises(ValueError):
            decode_hex("ABC")


if __name__ == "__main__":
    unittest.main()
