from src import utils
import argparse
import sys


def parse_args():
    """Argument parsing"""
    parser = argparse.ArgumentParser(
        description="Port Scanner")  # create parser object

    # Required Arguments
    parser.add_argument("target", help="Target IP address or hostname.")

    # Optional arguments
    parser.add_argument(
        "-p", "--port", help="Port(s) to scan (e.g. 80,223,1024,100-200)."
    )
    parser.add_argument(
        "-t", "--timeout", type=int, help="Timeout per port in seconds."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose/debug output."
    )
    parser.add_argument(
        "-b", "--banner", action="store_true", help="Grab banner of the port being scanned. Displays the services running on a port."
    )
    parser.add_argument(
        "-o", "--output", nargs='?', const="results.txt", type=str, help="Output results to txt file (default: results.txt)."
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Check if target is valid
    if utils.is_valid_ip(args.target):
        ip_address = args.target
    elif utils.is_valid_hostname(args.target):
        # Assign IP address to variable if resolution succeeds
        ip_address = utils.resolve_hostname(args.target)
        if not ip_address:
            sys.exit(1)  # Exit with error code if resolution fails
    else:
        sys.exit(1)

    # Parse ports if specified
    if args.port:
        try:
            port_list = utils.parse_ports(args.port)
        except Exception as e:
            print(f"Invalid port specification: {e}")
            sys.exit(1)
    else:
        # if no ports are specified, default to the top 1000 ports
        port_list = list(range(1, 1001))

    # Set timeout if specified
    if args.timeout:
        timeout = args.timeout
    else:
        timeout = 1

    # Scanning operations
    results = []  # Initialize list to store all the scanned ports
    try:
        for p in port_list:
            if args.verbose:
                print(f"Scanning port {p}...")
            if not args.banner:
                # Scan the target without banner grabbing and store True/False
                is_open = utils.scan_ip(ip_address, p, timeout)
                # Append the port number and status of the port (True = open, False = closed)
                results.append((p, is_open))
            else:
                is_open, banner = utils.banner_scan(ip_address, p, timeout)
                results.append((p, is_open, banner))
    except KeyboardInterrupt as e:
        print("\nScan interrupted by user")
        sys.exit(0)

    # If output arg is given, send to file
    if args.output:
        output_path = args.output
        try:
            with open(output_path, 'w') as f:
                f.write(utils.format_results(results))
            print(f"\nSuccessfully printed output to {output_path}")
            sys.exit(0)
        except IOError as e:
            print(f"\nError writing to {output_path}: {e}")
            sys.exit(0)
    else:
        # Otherwise, format the results and print
        utils.format_results(results)

    if args.verbose:
        print("\nScan complete")
