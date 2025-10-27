import socket
import sys


def scan_ports(ip_address, port):
    """Scans for open ports on a target IP address and returns true/false"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port))
            return True
    except (OSError, socket.error) as e:
        return False
    except socket.timeout as e:
        print(f"Socket timeout: {e}")
        return False


def is_port_open(ip_address, port):
    """Checks if a specific port is open on a target IP"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port))
            return True
    except (OSError, socket.error):
        return False
