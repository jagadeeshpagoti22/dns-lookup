
```ansi
[1;36m
██████╗ ███╗   ██╗███████╗██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██║██████╗
██╔══██╗████╗  ██║██╔════╝██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
██║  ██║██╔██╗ ██║███████╗██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
██║  ██║██║╚██╗██║╚════██║██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝
██████╔╝██║ ╚████║███████║███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║
╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝

              Professional DNS Intelligence & Reconnaissance CLI
[0m
```

# DNSLookup Professional CLI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: AGPLv3](https://img.shields.io/badge/License-AGPL_v3-purple.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![PyPI](https://img.shields.io/pypi/v/dnslookup-cli?color=3775A9&logo=pypi&logoColor=white)](https://pypi.org/project/dnslookup-cli/)

> Professional command-line DNS reconnaissance and lookup utility with rich terminal output, reverse DNS resolution, WHOIS integration, DNS tracing, and batch processing.

---

## Overview

DNSLookup Professional is a modern CLI-based DNS intelligence and reconnaissance tool built for developers, cybersecurity learners, penetration testers, and system administrators.

It provides fast, structured, and visually clean DNS query results directly in the terminal while supporting multiple DNS operations commonly used in network analysis and security investigations.

---

## Features

- Professional rich terminal UI
- Query DNS records:
  - A
  - AAAA
  - MX
  - NS
  - TXT
  - CNAME
  - SOA
- Reverse DNS lookup
- WHOIS domain intelligence lookup
- DNS resolution path tracing
- Batch domain lookup processing
- JSON output support
- Fast concurrent processing
- Clean professional CLI output

---

# Installation

Clone repository:

```bash
git clone https://github.com/yourusername/dns-lookup-professional-ui.git
```

Move into project directory:

```bash
cd dns-lookup-professional-ui
```

Create virtual environment:

### Linux / Kali

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install .
```

Or:

```bash
pip install -r requirements.txt
```

---

# Quick Start

Basic DNS query:

```bash
dnslookup query google.com
```

Reverse lookup:

```bash
dnslookup reverse 8.8.8.8
```

WHOIS lookup:

```bash
dnslookup whois tesla.com
```

Trace DNS resolution:

```bash
dnslookup trace github.com
```

Batch lookup:

```bash
dnslookup batch domains.txt
```

JSON output:

```bash
dnslookup query google.com --json
```

---

# Command Reference

| Command | Description |
|--------|-------------|
| `dnslookup query <domain>` | Query DNS records |
| `dnslookup reverse <ip>` | Reverse DNS lookup |
| `dnslookup whois <domain>` | Domain WHOIS lookup |
| `dnslookup trace <domain>` | Trace DNS resolution |
| `dnslookup batch <file>` | Batch lookup multiple domains |
| `dnslookup --help` | Show help |

---

# Example Output

### DNS Query

```bash
dnslookup query tesla.com
```

Returns:

- A records
- MX records
- NS records
- SOA records
- TTL information
- Response timing

---

# Use Cases

This tool is useful for:

- Cybersecurity reconnaissance
- DNS enumeration
- Threat intelligence investigations
- Infrastructure diagnostics
- Network troubleshooting
- Domain intelligence gathering
- Security learning labs

---

# Project Structure

```bash
dns-lookup-professional-ui/
│
├── dnslookup/
├── tests/
├── learn/
├── DEMO.md
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

# Requirements

- Python 3.10+
- pip
- Internet connection

Optional:

- uv
- just command runner

---

# License

Licensed under **AGPL v3.0**

---

# Author

Jagadeesh Pagoti
