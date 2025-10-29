import socket
import ipaddress


def scan_ip(ip_address, port):
    """Scans for open ports on a target IP address and returns true/false"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port))
            return True
    except (Exception, socket.error) as e:
        return False
    except socket.timeout as e:
        print(f"Socket timeout: {e}")
        return False


def scan_ip_timeout(ip_address, port, duration):
    """Scans for open port(s) within the timeout given"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port))
            s.settimeout(duration)
            return True
    except (Exception, socket.error) as e:
        return False
    except socket.timeout as e:
        print(f"Socket timeout: {e}")
        return False


def is_valid_ip(ip_address):
    """Checks if IP is valid"""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except (Exception, socket.error) as e:
        print(f"Error: {e}")
        return False


def is_valid_hostname(hostname):
    """Check if hostname is valid"""

    try:
        socket.gethostbyname(hostname)  # Resolve hostname to IP address
        return True
    except (socket.gaierror, socket.error) as e:
        print(f"Invalid hostname: {e}")
        return False


def resolve_hostname(hostname):
    """Resolve a hostname to an IP address"""

    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except (socket.gaierror, socket.error) as e:
        print(f"Error: {e}")
        return False


def parse_ports(ports):
    """Parse the ports from args"""

    # Check if it is multiple ports, single port, or range
    if "," in ports:  # If it is comma-separated ports
        port_list = int(ports.split(','))
    elif '-' in ports:  # If it is a range of ports
        port_split = int(ports.split('-'))

        for p in range(port_split[0], port_split[1]):
            port_list.append(p)
    else:
        return False  # If input is invalid return False

    return port_list
