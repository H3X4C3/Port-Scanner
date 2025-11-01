import socket
import ipaddress


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


def banner_scan(ip_address, port, timeout):
    """Scans for open port(s) and grabs the services running on the port(s)"""

    # Try protocol-specific helpers; they return (is_open, banner)
    for helper in (banner_ftp, banner_http, banner_ssh):
        try:
            is_open, banner = helper(ip_address, port, timeout)
        except Exception:
            is_open, banner = False, None

        if is_open:
            return True, banner

    # Generic fallback
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip_address, port))
            try:
                s.send(b'\r\n')
                data = s.recv(1024)
                if data:
                    banner = data.decode(errors='ignore').strip()
                    return True, banner
                return True, None  # connected but no banner
            except socket.timeout:
                return True, None
    except (socket.error, socket.timeout):
        return False, None


def banner_http(ip_address, port, timeout):
    """Grab banner for HTTP/HTTPS ports"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip_address, port))
            # Set the HTTP request
            request = b"GET / HTTP/1.1\r\nHost: " + ip_address.encode() + b"\r\n\r\n"
            s.send(request)
            response = s.recv(1024)

            if response:
                banner = response.decode(errors='ignore').strip()
                # Store the HTTP response and split it by line
                lines = banner.split("\n")
                # return status line
                return True, lines[0] if lines else banner
            return True, None
    except (socket.error, socket.timeout):
        return False, None


def banner_ssh(ip_address, port, timeout):
    """Grab banner for SSH ports"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip_address, port))
            data = s.recv(1024)
            if data:
                banner = data.decode(errors='ignore').strip()
                return True, banner
            return True, None
    except (socket.error, socket.timeout):
        return False, None


def banner_ftp(ip_address, port, timeout):
    """Grab banner for FTP ports"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip_address, port))
            # Try to immediately get response
            data = s.recv(1024)
            if data:
                banner = data.decode(errors='ignore').strip()
                return True, banner
            # If no immediate response
            s.send(b"USER anonymous\r\n")
            data = s.recv(1024)
            if data:
                banner = data.decode(errors='ignore').strip()
                return True, banner
            return True, None
    except (socket.error, socket.timeout):
        return False, None


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


def format_results(results):
    """Formats and prints scan results in a tabular format"""

    has_banner = len(results) > 0 and len(
        results[0]) == 3  # Check if banners are included

    print("\n")
    if has_banner:
        print(f"{'Port':<12} {'Status':<12} {'Banner'}")
        print("-" * 40)
        for port, is_open, banner in results:
            status = "Open" if is_open else "Closed"
            banner_str = banner if banner else "N/A"
            print(f"{port:<12} {status:<12} {banner_str}")
    else:
        print(f"{'Port':<12} {'Status':<12}")
        print("-" * 26)
        for port, is_open in results:
            status = "Open" if is_open else "Closed"
            print(f"{port:<12} {status:<12}")
    print("\n")
