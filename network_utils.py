import ipaddress
import socket
import subprocess

import psutil


def _get_default_route_interface_ip_windows():

    risultato = subprocess.run(
        ["route", "print", "0.0.0.0"],
        capture_output=True,
        text=True,
        check=False,
    )

    in_ipv4_table = False
    in_active_routes = False

    for raw_line in risultato.stdout.splitlines():
        line = raw_line.strip()

        if line.startswith("IPv4 Tabella route") or line.startswith("IPv4 Route Table"):
            in_ipv4_table = True
            in_active_routes = False
            continue

        if in_ipv4_table and (line.startswith("Route attive:") or line.startswith("Active Routes:")):
            in_active_routes = True
            continue

        if in_ipv4_table and in_active_routes and line.startswith("0.0.0.0"):
            parts = line.split()
            if len(parts) >= 5:
                return parts[3]

    return None


def get_local_network():

    default_interface_ip = _get_default_route_interface_ip_windows()

    if default_interface_ip:
        for addresses in psutil.net_if_addrs().values():
            for addr in addresses:
                if addr.family != socket.AF_INET:
                    continue

                if addr.address != default_interface_ip:
                    continue

                if addr.address.startswith("127."):
                    continue

                return ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}",
                    strict=False,
                )

    candidate = None

    for interface, addresses in psutil.net_if_addrs().items():

        name = interface.lower()

        # Ignore common virtual interfaces
        if any(x in name for x in [
            "virtual",
            "vmware",
            "vbox",
            "virtualbox",
            "hyper-v",
            "docker",
            "loopback",
            "vethernet"
        ]):
            continue

        for addr in addresses:

            if addr.family != socket.AF_INET:
                continue

            ip = addr.address
            mask = addr.netmask

            if ip.startswith("127."):
                continue

            network = ipaddress.IPv4Network(
                f"{ip}/{mask}",
                strict=False
            )

            candidate = network

            # Prefer common private networks
            if (
                ip.startswith("192.168.")
                or ip.startswith("10.")
                or ip.startswith("172.")
            ):
                return network

    return candidate