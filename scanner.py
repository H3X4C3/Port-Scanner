import socket
import sys
from src import utils


try:
    for port in range(1, 1024):
        result = utils.scan_ip('localhost', port)

        if result:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
except KeyboardInterrupt:
    print("\nScan interrupted by user.\n")
    sys.exit(0)

# result = utils.scan_ports('localhost', 135)

# if result:
#     print(f"Port 135 is open")
# else:
#     print(f"Port 135 is closed")
