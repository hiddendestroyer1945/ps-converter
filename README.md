# Port-Service Converter (ps-converter)

A helpful utility for network engineers and students to convert between TCP/UDP port numbers and service names, fetching the latest official registry data directly from IANA.

## Features

*   **Bidirectional Conversion**:
    *   **Port to Service**: Enter a port number (e.g., `80`) to see the associated service name and description for both TCP and UDP.
    *   **Service to Port**: Enter a service name (e.g., `ssh`) to see the standard port number and description.
*   **Live Data**: Automatically downloads the latest *Service Name and Transport Protocol Port Number Registry* from IANA on startup.
*   **Interactive Interface**: Simple command-line loop for quick lookups.
*   **Validation**: Checks for valid port ranges (0-64738).

## Requirements

*   **Operating System**: Developed for **Debian Linux** based distributions (e.g., Ubuntu, Kali, Mint).
*   **Python 3.x**
*   **Git**
*   **Internet Connection** (required to fetch the IANA registry CSV)

## Installation

Install the necessary dependencies and clone the repository:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 git
git clone https://github.com/hiddendestroyer1945/code-projects.git
cd ps-converter/
```

## Usage

Run the script using Python:

```bash
python3 ps-converter.py
```

### Example Session

```text
Downloading service registry from https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv...
Download complete. Parsing data...
Ready.

Enter port number or service name (or 'q' to quit): 80

Information for Port 80:
  TCP: Service='http', Description='World Wide Web HTTP'
  UDP: Service='http', Description='World Wide Web HTTP'

Enter port number or service name (or 'q' to quit): ssh

Information for Service 'ssh':
  Description: The Secure Shell (SSH) Protocol
  TCP Port: 22
  UDP Port: 22
```

## How it Works

The tool fetches the CSV file from `https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv`. It parses this file to build a lookup table for all defined TCP and UDP services, allowing for accurate and up-to-date information without relying on potentially outdated local system files (like `/etc/services`).
