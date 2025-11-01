# Port-Scanner

A small, easy-to-use TCP port scanner written in Python. It’s lightweight, depends only on the standard library, and is built for quick checks, learning, and basic troubleshooting. It can scan single ports, lists of ports, or ranges, and can optionally grab simple service banners.

---

## What’s included

- scanner.py — program entrypoint
- src/cli.py — command-line interface and scan orchestration
- src/utils.py — network helpers, banner probes, argument parsing, and output formatting

---

## Requirements

- Python 3.7 or newer

No third-party packages required.

---

## Quick start

1. Clone the repo:
   `git clone https://github.com/H3X4C3/Port-Scanner.git`

2. Change into the project folder:
   `cd Port-Scanner`

3. Run the scanner:
   `python scanner.py <target> [options]`

---

## Usage

`python scanner.py <target> [-p PORTS] [-t TIMEOUT] [-b] [-v] [-o OUTPUT]`

```
Arguments
- target — hostname or IP address to scan

Options
- -p, --port — ports to scan. Examples:
  - Single port: 22
  - Multiple ports: 22,80,443
  - Range: 1-1024
  If omitted, the scanner checks ports 1–1000.
- -t, --timeout — timeout in seconds per port (default 1)
- -b, --banner — enable banner grabbing; results include banner text when available
- -v, --verbose — show progress messages while scanning
- -o, --output — write results to a file (supports .txt)
```

---

## Examples

- Scan the default top 1000 ports:
  `python scanner.py 192.168.1.10`

- Scan ports 22, 80 and 443:
  `python scanner.py example.com -p 22,80,443`

- Scan a range with banners and longer timeout:
  `python scanner.py 10.0.0.5 -p 1-1024 -b -t 2 -v`

---

## How it works

- The scanner performs TCP connect scans by attempting to open a socket on each port and reporting whether the connection succeeds.
- Banner grabbing includes some protocol-aware probes for HTTP, SSH, and FTP, with a generic fallback for other services.
- Output is printed as a simple table. When banner grabbing is enabled, the banner is shown alongside each port’s status.

---

## Notes, limitations and tips

- This is a connect-based scanner. It is reliable but not stealthy.
- Scanning lots of ports sequentially can be slow. Consider adding threading or asyncio to speed up large scans.
- Banner parsing is minimal and may not always identify services correctly.
- The output file option is available from the CLI; review the code if you need a specific format or behavior.

---

## Responsible use

Do not scan systems without explicit permission. Unauthorized scanning may be illegal or violate acceptable use policies. Always get written permission before performing active scans on systems you do not own.

---

## Contributing

Suggestions, bug reports, and pull requests are welcome. Ideas:
- Add concurrency for faster scans
- Add UDP scanning
- Improve banner parsing and output formats

---

## License

[MIT License](LICENSE)
