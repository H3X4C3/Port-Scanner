import socket
import ipaddress


# def scan_ip(ip_address, port):
#     """Scans for open ports on a target IP address and returns true/false"""

#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((ip_address, port))
#             return True
#     except (Exception, socket.error) as e:
#         return False
#     except socket.timeout as e:
#         print(f"Socket timeout: {e}")
#         return False


def scan_ip(ip_address, port, timeout):
    """Scans for open port(s) within the timeout given"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip_address, port))
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
    except ValueError:
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
    port_list = []

    try:
        # Check if it is multiple ports, single port, or range
        if "," in ports:  # If it is comma-separated ports
            # Separates white spaces and converts the strings to int
            port_list = [int(p.strip()) for p in ports.split(',')]
        elif '-' in ports:  # If it is a range of ports
            start, end = [int(p.strip()) for p in ports.split('-')]
            port_list = list(range(start, end + 1))
        else:  # Otherwise if a single port was specified
            port_list = [int(ports.strip())]

        # Make sure the port numbers are within range of 1-65535
        for port in port_list:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} is out of range (1-65535)!")
    except (ValueError, TypeError) as e:
        # Re-raise with a clearer message
        raise ValueError(f"Invalid port specification '{ports}': {e}") from e
    except Exception as e:
        raise ValueError(f"Error parsing ports '{ports}': {e}") from e

    return port_list
