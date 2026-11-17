"""NetTools — CCNA 1 Networking Toolkit desktop application."""

import ipaddress
import random
import threading

import customtkinter as ctk

from modules.cisco_generator import generate_interface_config
from modules.encoding_tools import decode_base64, decode_hex, encode_base64, encode_hex
from modules.ipv6_tools import compress_ipv6, expand_ipv6
from modules.mac_converter import convert_mac_address
from modules.route_tools import summarize_routes
from modules.socket_tester import test_tcp_connection
from modules.subnet_tools import analyze_subnet
from modules.transfer_calculator import calculate_transfer_seconds, format_duration


BACKGROUND = "#0B1120"
SIDEBAR = "#111B2E"
CARD = "#17243A"
ACCENT = "#38BDF8"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"

TOOLS = {
    "IPv6 Tools": ("IPv6 Compressor / Decompressor", "Format a valid IPv6 address in compressed or expanded form."),
    "Subnet Validator": ("Subnet Mask Validator", "Check an IPv4 subnet mask and calculate network details."),
    "Route Calculator": ("Route Summarization", "Collapse IPv4 CIDR routes into a compact route list."),
    "Transfer Calculator": ("Transfer Time Calculator", "Estimate ideal transfer duration from file size and link speed."),
    "Cisco Generator": ("Cisco Configuration Generator", "Generate IOS commands for one IPv4 interface."),
    "MAC Converter": ("MAC Address Converter", "Convert a 48-bit MAC address to common notations."),
    "Socket Tester": ("TCP Socket Tester", "Check one authorized TCP host and port."),
    "Encoding Tools": ("Base64 & Hex Converter", "Encode or decode UTF-8 text using Base64 or hexadecimal."),
}


class NetToolsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NetTools | CCNA 1 Networking Toolkit")
        self.geometry("1180x760")
        self.minsize(940, 620)
        self.configure(fg_color=BACKGROUND)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.sidebar_buttons = {}
        self._create_sidebar()
        self.main_area = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.main_area.pack(side="right", fill="both", expand=True)
        self.show_dashboard()

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=235, corner_radius=0, fg_color=SIDEBAR)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        ctk.CTkLabel(
            sidebar, text="NETTOOLS", font=("Arial", 25, "bold"), text_color=ACCENT
        ).pack(pady=(28, 4))
        ctk.CTkLabel(
            sidebar, text="CCNA 1 NETWORKING TOOLKIT", font=("Arial", 10), text_color=MUTED
        ).pack(pady=(0, 25))

        for name in ("Dashboard", *TOOLS.keys()):
            button = ctk.CTkButton(
                sidebar,
                text=name,
                height=40,
                corner_radius=8,
                anchor="w",
                fg_color="transparent",
                hover_color="#253550",
                text_color="#E2E8F0",
                font=("Arial", 13),
                command=lambda selected=name: self.navigate(selected),
            )
            button.pack(fill="x", padx=13, pady=3)
            self.sidebar_buttons[name] = button

        footer = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=17, pady=19)
        ctk.CTkLabel(
            footer, text="DEVELOPED BY", font=("Arial", 10, "bold"), text_color="#64748B"
        ).pack(anchor="w")
        ctk.CTkLabel(
            footer,
            text="Nourcine Gharbi\nWael Mbarki",
            font=("Arial", 12, "bold"),
            text_color=TEXT,
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

    def _clear(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def _select_nav(self, selected):
        for name, button in self.sidebar_buttons.items():
            button.configure(fg_color="#1D3553" if name == selected else "transparent")

    def navigate(self, page):
        if page == "Dashboard":
            self.show_dashboard()
        else:
            self.show_tool_page(page)

    def _scroll_area(self):
        body = ctk.CTkScrollableFrame(
            self.main_area, fg_color=BACKGROUND, corner_radius=0
        )
        body.pack(fill="both", expand=True)
        return body

    def show_dashboard(self):
        self._clear()
        self._select_nav("Dashboard")
        body = self._scroll_area()
        ctk.CTkLabel(
            body, text="Welcome to NetTools", font=("Arial", 31, "bold"), text_color=TEXT
        ).pack(anchor="w", padx=35, pady=(32, 4))
        ctk.CTkLabel(
            body,
            text="Your all-in-one CCNA 1 networking assistant.",
            font=("Arial", 14),
            text_color=MUTED,
        ).pack(anchor="w", padx=35, pady=(0, 18))

        intro = ctk.CTkFrame(body, fg_color=CARD, corner_radius=15)
        intro.pack(fill="x", padx=35, pady=8)
        ctk.CTkLabel(
            intro, text="NETWORKING MADE SIMPLE", font=("Arial", 19, "bold"), text_color=ACCENT
        ).pack(anchor="w", padx=22, pady=(18, 5))
        ctk.CTkLabel(
            intro,
            text="Practice essential addressing, routing, encoding, and connectivity concepts.\n"
            "Developed by Nourcine Gharbi and Wael Mbarki.",
            font=("Arial", 13),
            text_color="#CBD5E1",
            justify="left",
        ).pack(anchor="w", padx=22, pady=(3, 18))

        ctk.CTkLabel(
            body, text="AVAILABLE TOOLS", font=("Arial", 18, "bold"), text_color=TEXT
        ).pack(anchor="w", padx=35, pady=(18, 5))
        cards = ctk.CTkFrame(body, fg_color="transparent")
        cards.pack(fill="both", expand=True, padx=27, pady=3)
        for index, (name, (title, description)) in enumerate(TOOLS.items()):
            row, column = divmod(index, 2)
            card = ctk.CTkFrame(
                cards, fg_color=CARD, corner_radius=12, border_width=1, border_color="#263B56"
            )
            card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")
            ctk.CTkLabel(
                card, text=name.upper(), font=("Arial", 10, "bold"), text_color=ACCENT
            ).pack(anchor="w", padx=15, pady=(13, 3))
            ctk.CTkLabel(
                card, text=title, font=("Arial", 15, "bold"), text_color=TEXT
            ).pack(anchor="w", padx=15, pady=2)
            ctk.CTkLabel(
                card,
                text=description,
                font=("Arial", 12),
                text_color=MUTED,
                wraplength=350,
                justify="left",
            ).pack(anchor="w", padx=15, pady=(2, 8))
            ctk.CTkButton(
                card,
                text="Open tool",
                height=31,
                fg_color="#0369A1",
                hover_color="#0284C7",
                command=lambda selected=name: self.navigate(selected),
            ).pack(anchor="w", padx=15, pady=(2, 13))
        cards.grid_columnconfigure((0, 1), weight=1)
        cards.grid_rowconfigure((0, 1, 2, 3), weight=1)

    def _page(self, page):
        self._clear()
        self._select_nav(page)
        body = self._scroll_area()
        title, description = TOOLS[page]
        ctk.CTkLabel(
            body, text=title, font=("Arial", 28, "bold"), text_color=ACCENT
        ).pack(anchor="w", padx=35, pady=(34, 5))
        ctk.CTkLabel(
            body,
            text=description,
            font=("Arial", 13),
            text_color=MUTED,
            wraplength=780,
            justify="left",
        ).pack(anchor="w", padx=35, pady=(0, 17))
        panel = ctk.CTkFrame(body, fg_color=CARD, corner_radius=14)
        panel.pack(fill="x", padx=35, pady=6)
        return panel

    @staticmethod
    def _label(parent, text):
        ctk.CTkLabel(parent, text=text, font=("Arial", 12, "bold"), text_color="#CBD5E1").pack(
            anchor="w", padx=20, pady=(12, 4)
        )

    def _entry(self, parent, label, placeholder=""):
        self._label(parent, label)
        entry = ctk.CTkEntry(
            parent,
            height=38,
            placeholder_text=placeholder,
            fg_color="#0F1A2B",
            border_color="#334155",
        )
        entry.pack(fill="x", padx=20, pady=(0, 3))
        return entry

    def _textbox(self, parent, label="Result"):
        self._label(parent, label)
        output = ctk.CTkTextbox(
            parent, height=145, fg_color="#0F1A2B", border_width=1, border_color="#334155"
        )
        output.pack(fill="x", padx=20, pady=(0, 18))
        output.configure(state="disabled")
        return output

    @staticmethod
    def _write(output, text):
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", text)
        output.configure(state="disabled")

    @staticmethod
    def _action_button(parent, text, command):
        ctk.CTkButton(
            parent,
            text=text,
            height=38,
            fg_color="#0369A1",
            hover_color="#0284C7",
            command=command,
        ).pack(anchor="w", padx=20, pady=(14, 3))

    @staticmethod
    def _set_entry(entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value))

    def _sample_button(self, parent, command, text="Generate random fields"):
        ctk.CTkButton(
            parent,
            text=text,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=command,
        ).pack(anchor="w", padx=20, pady=(9, 15))

    def _error(self, output, error):
        self._write(output, f"Error: {error}")

    def show_tool_page(self, page):
        panel = self._page(page)
        builder = {
            "IPv6 Tools": self._ipv6_page,
            "Subnet Validator": self._subnet_page,
            "Route Calculator": self._routes_page,
            "Transfer Calculator": self._transfer_page,
            "Cisco Generator": self._cisco_page,
            "MAC Converter": self._mac_page,
            "Socket Tester": self._socket_page,
            "Encoding Tools": self._encoding_page,
        }[page]
        builder(panel)

    def _ipv6_page(self, panel):
        address = self._entry(panel, "IPv6 address", "2001:db8::1")
        output = self._textbox(panel)

        def run(converter):
            try:
                self._write(output, converter(address.get()))
            except ValueError as exc:
                self._error(output, exc)

        buttons = ctk.CTkFrame(panel, fg_color="transparent")
        buttons.pack(anchor="w", padx=20, pady=(12, 0))
        ctk.CTkButton(buttons, text="Compress", command=lambda: run(compress_ipv6)).pack(
            side="left", padx=(0, 8)
        )
        ctk.CTkButton(buttons, text="Expand", command=lambda: run(expand_ipv6)).pack(side="left")

        def random_fields():
            address_value = ipaddress.IPv6Address(random.getrandbits(128))
            self._set_entry(address, address_value.compressed)
            self._write(output, "Random valid IPv6 address generated.")

        self._sample_button(panel, random_fields)

    def _subnet_page(self, panel):
        address = self._entry(panel, "IPv4 address", "192.168.1.25")
        mask = self._entry(panel, "Subnet mask", "255.255.255.0")
        output = self._textbox(panel)

        def calculate():
            try:
                details = analyze_subnet(address.get(), mask.get())
                lines = (
                    f"Network: {details['network']}\n"
                    f"Network address: {details['network_address']}\n"
                    f"Broadcast address: {details['broadcast_address']}\n"
                    f"Prefix length: /{details['prefix_length']}\n"
                    f"Total addresses: {details['total_addresses']}\n"
                    f"Usable hosts: {details['usable_hosts']}\n"
                    f"Usable range: {details['first_usable']} – {details['last_usable']}"
                )
                self._write(output, lines)
            except ValueError as exc:
                self._error(output, exc)

        self._action_button(panel, "Validate and calculate", calculate)

        def random_fields():
            self._set_entry(address, f"10.{random.randrange(256)}.{random.randrange(256)}.{random.randrange(1, 255)}")
            self._set_entry(mask, "255.255.255.0")
            self._write(output, "Random valid IPv4 address and subnet mask generated.")

        self._sample_button(panel, random_fields)

    def _routes_page(self, panel):
        self._label(panel, "IPv4 routes (one CIDR network per line)")
        routes = ctk.CTkTextbox(panel, height=125, fg_color="#0F1A2B", border_color="#334155")
        routes.pack(fill="x", padx=20, pady=(0, 3))
        routes.insert("1.0", "192.168.0.0/24\n192.168.1.0/24")
        output = self._textbox(panel)

        def calculate():
            try:
                result = summarize_routes(routes.get("1.0", "end").splitlines())
                self._write(output, "Summarized routes:\n" + "\n".join(result))
            except ValueError as exc:
                self._error(output, exc)

        self._action_button(panel, "Summarize routes", calculate)

        def random_fields():
            third_octet = random.randrange(128) * 2
            second_octet = random.randrange(256)
            routes.delete("1.0", "end")
            routes.insert(
                "1.0",
                f"10.{second_octet}.{third_octet}.0/24\n"
                f"10.{second_octet}.{third_octet + 1}.0/24",
            )
            self._write(output, "Two adjacent random /24 routes generated.")

        self._sample_button(panel, random_fields)

    def _transfer_page(self, panel):
        size = self._entry(panel, "File size", "100")
        size_unit = ctk.CTkOptionMenu(panel, values=["B", "KB", "MB", "GB"])
        size_unit.set("MB")
        self._label(panel, "File size unit")
        size_unit.pack(anchor="w", padx=20, pady=(0, 3))
        rate = self._entry(panel, "Network speed", "100")
        rate_unit = ctk.CTkOptionMenu(panel, values=["Kbps", "Mbps", "Gbps"])
        rate_unit.set("Mbps")
        self._label(panel, "Network speed unit")
        rate_unit.pack(anchor="w", padx=20, pady=(0, 3))
        output = self._textbox(panel)

        def calculate():
            try:
                seconds = calculate_transfer_seconds(
                    float(size.get()), size_unit.get(), float(rate.get()), rate_unit.get()
                )
                self._write(
                    output,
                    f"Ideal transfer time: {format_duration(seconds)}\n"
                    f"({seconds:.3f} seconds; excludes protocol overhead and real-world variation)",
                )
            except (ValueError, OverflowError) as exc:
                self._error(output, exc if isinstance(exc, ValueError) else "Values are too large.")

        self._action_button(panel, "Calculate transfer time", calculate)

        def random_fields():
            self._set_entry(size, random.randint(1, 900))
            self._set_entry(rate, random.randint(10, 1000))
            size_unit.set(random.choice(["MB", "GB"]))
            rate_unit.set(random.choice(["Mbps", "Gbps"]))
            self._write(output, "Random positive file size and link speed generated.")

        self._sample_button(panel, random_fields)

    def _cisco_page(self, panel):
        hostname = self._entry(panel, "Hostname", "R1")
        interface = self._entry(panel, "Interface", "GigabitEthernet0/0")
        address = self._entry(panel, "IPv4 address", "192.168.1.1")
        mask = self._entry(panel, "Subnet mask", "255.255.255.0")
        description = self._entry(panel, "Description (optional)", "LAN")
        output = self._textbox(panel, "Generated Cisco IOS configuration")

        def generate():
            try:
                config = generate_interface_config(
                    hostname.get(), interface.get(), address.get(), mask.get(), description.get()
                )
                self._write(output, config)
            except ValueError as exc:
                self._error(output, exc)

        self._action_button(panel, "Generate configuration", generate)

        def random_fields():
            self._set_entry(hostname, f"R{random.randint(1, 99)}")
            self._set_entry(interface, f"GigabitEthernet0/{random.randint(0, 3)}")
            self._set_entry(
                address,
                f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            )
            self._set_entry(mask, "255.255.255.0")
            self._set_entry(description, "NetTools test interface")
            self._write(output, "Random valid Cisco interface settings generated.")

        self._sample_button(panel, random_fields)

    def _mac_page(self, panel):
        address = self._entry(panel, "MAC address", "00:1A:2B:3C:4D:5E")
        output = self._textbox(panel)

        def convert():
            try:
                formats = convert_mac_address(address.get())
                self._write(
                    output,
                    f"Colon: {formats['colon']}\nHyphen: {formats['hyphen']}\n"
                    f"Cisco dotted: {formats['cisco']}\nUppercase: {formats['uppercase']}",
                )
            except ValueError as exc:
                self._error(output, exc)

        self._action_button(panel, "Convert MAC address", convert)

        def random_fields():
            octets = [0x02] + [random.randrange(256) for _ in range(5)]
            self._set_entry(address, ":".join(f"{octet:02X}" for octet in octets))
            self._write(output, "Random locally administered MAC address generated.")

        self._sample_button(panel, random_fields)

    def _socket_page(self, panel):
        host = self._entry(panel, "Authorized hostname or IP address", "example.com")
        port = self._entry(panel, "TCP port", "443")
        timeout = self._entry(panel, "Timeout in seconds (max 10)", "3")
        output = self._textbox(panel, "Connection result")
        self._write(
            output,
            "This performs one TCP connection attempt to the exact host and port you enter. "
            "Use only systems you own or are authorized to test.",
        )

        def check():
            try:
                port_value = int(port.get())
                timeout_value = float(timeout.get())
                if timeout_value > 10:
                    raise ValueError("Timeout must not exceed 10 seconds.")
                self._write(output, "Attempting one connection…")
            except ValueError as exc:
                self._error(output, exc)
                return

            def connect():
                try:
                    elapsed = test_tcp_connection(host.get(), port_value, timeout_value)
                    result = f"Connection succeeded to {host.get().strip()}:{port_value}\nElapsed: {elapsed:.3f} s"
                except (ValueError, OSError) as exc:
                    result = f"Connection failed: {exc}"
                self.after(0, lambda: self._write(output, result))

            threading.Thread(target=connect, daemon=True).start()

        self._action_button(panel, "Test this TCP connection", check)

        def random_fields():
            self._set_entry(host, "127.0.0.1")
            self._set_entry(port, random.randint(49152, 65535))
            self._set_entry(timeout, "1")
            self._write(
                output,
                "Local-only sample generated. The connection succeeds only if a service "
                "is listening on that randomly selected port.",
            )

        self._sample_button(panel, random_fields)

    def _encoding_page(self, panel):
        self._label(panel, "Text or encoded input")
        source = ctk.CTkTextbox(panel, height=125, fg_color="#0F1A2B", border_color="#334155")
        source.pack(fill="x", padx=20, pady=(0, 3))
        output = self._textbox(panel)

        def transform(operation):
            try:
                self._write(output, operation(source.get("1.0", "end-1c")))
            except ValueError as exc:
                self._error(output, exc)

        button_row = ctk.CTkFrame(panel, fg_color="transparent")
        button_row.pack(anchor="w", padx=20, pady=(12, 0))
        choices = (
            ("Base64 encode", encode_base64),
            ("Base64 decode", decode_base64),
            ("Hex encode", encode_hex),
            ("Hex decode", decode_hex),
        )
        for label, operation in choices:
            ctk.CTkButton(
                button_row,
                text=label,
                width=130,
                command=lambda selected=operation: transform(selected),
            ).pack(side="left", padx=(0, 7), pady=2)

        def random_text():
            sample = f"NetTools test {random.randint(1000, 9999)}"
            source.delete("1.0", "end")
            source.insert("1.0", sample)
            self._write(output, "Random plain-text input generated for encoding.")

        def random_base64():
            sample = f"NetTools test {random.randint(1000, 9999)}"
            source.delete("1.0", "end")
            source.insert("1.0", encode_base64(sample))
            self._write(output, "Random valid Base64 input generated for decoding.")

        def random_hex():
            sample = f"NetTools test {random.randint(1000, 9999)}"
            source.delete("1.0", "end")
            source.insert("1.0", encode_hex(sample))
            self._write(output, "Random valid hexadecimal input generated for decoding.")

        sample_row = ctk.CTkFrame(panel, fg_color="transparent")
        sample_row.pack(anchor="w", padx=20, pady=(9, 15))
        for label, callback in (
            ("Random text", random_text),
            ("Random Base64", random_base64),
            ("Random Hex", random_hex),
        ):
            ctk.CTkButton(
                sample_row,
                text=label,
                height=34,
                fg_color="#334155",
                hover_color="#475569",
                command=callback,
            ).pack(side="left", padx=(0, 8))


if __name__ == "__main__":
    app = NetToolsApp()
    app.mainloop()
