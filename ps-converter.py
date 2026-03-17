
import sys
import urllib.request
import csv
import io

def load_services():
    """
    Fetches IANA service registry from the internet and builds mapping dictionaries.
    Returns:
        port_service_map: { port_num: {'tcp': {'name': str, 'desc': str}, 'udp': ...} }
        service_port_map: { service_name: {'tcp': port_num, 'udp': port_num, 'desc': str} }
    """
    url = "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"
    print(f"Downloading service registry from {url}...")
    
    port_service_map = {}
    service_port_map = {}

    try:
        with urllib.request.urlopen(url) as response:
            csv_content = response.read().decode('utf-8')
        
        print("Download complete. Parsing data...")
        
        # Use csv module to parse
        f = io.StringIO(csv_content)
        reader = csv.reader(f)
        
        # Skip header if present (first row usually has "Service Name" etc)
        # We can detect header by checking the first cell
        header = next(reader, None)
        
        # Checking just in case the first line isn't the header or it's empty
        if header and header[0] != 'Service Name':
            # convert back to list to iterate if it wasn't a header? 
            # Actually IANA CSV always has a header. Let's assume standard format.
            pass

        for row in reader:
            if len(row) < 4:
                continue
            
            # Columns: Service Name (0), Port Number (1), Transport Protocol (2), Description (3)
            service_name = row[0].strip()
            port_str = row[1].strip()
            protocol = row[2].strip().lower()
            description = row[3].strip()

            # We need at least a port and a protocol
            if not port_str or not protocol:
                continue
            
            # Protocol must be tcp or udp for this tool
            if protocol not in ('tcp', 'udp'):
                continue

            try:
                port = int(port_str)
            except ValueError:
                # Some ranges like "1-5" or references exist, skip them for now or handle simple ints
                continue

            # Populate Port -> Service Map
            if port not in port_service_map:
                port_service_map[port] = {}
            
            # Only overwrite if not present or if we have a name and the previous one didn't?
            # IANA list might have multiple entries. We'll take the first valid one or last one.
            # Usually strict duplicates aren't an issue for major services.
            # Use 'setdefault' logic or just overwrite.
            # Let's preserve existing if the new one is empty name
            
            if protocol not in port_service_map[port] or (service_name and not port_service_map[port][protocol]['name']):
                port_service_map[port][protocol] = {
                    'name': service_name,
                    'desc': description
                }

            # Populate Service -> Port Map
            if service_name:
                # Use lowercase for case-insensitive lookup storage if desired, 
                # but let's store original key for display and lower for lookup.
                # Here we just store the name as is.
                
                if service_name not in service_port_map:
                    service_port_map[service_name] = {'desc': description}
                
                service_port_map[service_name][protocol] = port
                # Update description if the new one is longer/better? Key first one.
                if description and not service_port_map[service_name]['desc']:
                     service_port_map[service_name]['desc'] = description

    except Exception as e:
        print(f"Error fetching or parsing services: {e}")
        sys.exit(1)

    return port_service_map, service_port_map

def main():
    port_map, service_map = load_services()
    print("Ready.")

    while True:
        try:
            user_input = input("\nEnter port number or service name (or 'q' to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if user_input.lower() in ('q', 'quit', 'exit'):
            break
        
        if not user_input:
            continue

        # Check if input is a number (Port)
        if user_input.isdigit():
            port = int(user_input)
            if not (0 <= port <= 64738):
                print("Error: Port number out of range (0-64738).")
                continue
            
            print(f"\nInformation for Port {port}:")
            
            found_any = False
            if port in port_map:
                if 'tcp' in port_map[port]:
                    data = port_map[port]['tcp']
                    print(f"  TCP: Service='{data['name']}', Description='{data['desc']}'")
                    found_any = True
                else:
                    print(f"  TCP: No specific service mapped.")

                if 'udp' in port_map[port]:
                    data = port_map[port]['udp']
                    print(f"  UDP: Service='{data['name']}', Description='{data['desc']}'")
                    found_any = True
                else:
                    print(f"  UDP: No specific service mapped.")
            else:
                 print("  No known services for this port in IANA registry.")
                 
        # Treat as Service Name
        else:
            service_name = user_input
            
            match = None
            # Direct match
            if service_name in service_map:
                match = service_map[service_name]
            else:
                # Case-insensitive search
                for name in service_map:
                    if name.lower() == service_name.lower():
                        match = service_map[name]
                        service_name = name # Update to matched case
                        break
            
            if match:
                print(f"\nInformation for Service '{service_name}':")
                desc = match.get('desc', '')
                if desc:
                    print(f"  Description: {desc}")
                
                if 'tcp' in match:
                    print(f"  TCP Port: {match['tcp']}")
                else:
                    print("  TCP Port: Not defined")
                
                if 'udp' in match:
                    print(f"  UDP Port: {match['udp']}")
                else:
                    print("  UDP Port: Not defined")
            else:
                print(f"Service '{service_name}' not found.")

if __name__ == "__main__":
    main()
