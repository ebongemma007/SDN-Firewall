# SDN-based Firewall with Ryu Controller

## Description
This project demonstrates a basic SDN-based firewall implemented using the Ryu controller and Mininet. The firewall blocks traffic based on specific IP addresses, ports, and protocols (such as ICMP). It also logs dropped packets for auditing purposes.

## Features
- **ICMP (Ping) blocking**: Blocks all ICMP traffic between hosts.
- **Port-based filtering**: Blocks specific TCP/UDP ports (e.g., SSH, HTTP).
- **IP-based filtering**: Blocks traffic from/to specific IP addresses.
- **Traffic logging**: Logs blocked packets for audit purposes.

## Network Topology
The network consists of:
- 2 hosts (h1, h2)
- 1 OpenFlow switch (s1)
- Ryu controller managing the firewall rules.

## Requirements
- Mininet
- Ryu controller

## Setup Instructions
1.**Clone this repository**:
   ```bash
   git clone https://github.com/ebongemma007/SDN-Firewall
```
2.**Install Ryu**:
   ```bash
   sudo apt update
   sudo apt install python3-ryu
```
3. **Run the Ryu Firewall Application**: Start the Ryu controller and run the firewall application
```bash
   ryu-manager firewall.py
```
5. **Start Mininet with Custom Topology**: Use the provided topology script to launch Mininet
```bash
   sudo python3 sdn_topology.py
```
7. **Test the Network**: Ping hosts to verify ICMP blocking
```bash
   mininet> h1 ping h2
```
   You can also test port-based filtering using tools like **netcat** or attempt an SSH connection
   ```bash
   mininet> h1 nc -l 80
   mininet> h2 nc h1 80
```

 **Advanced Features**:
  
   **Blocking Ports**: Modify the **firewall.py** file to add or remove ports from the **self.blocked_ports** list.
   **Blocking IPs**: Add or remove IP addresses from the **self.blocked_ips** list in the **firewall.py** file.

**Testing**:
Use Mininet's CLI to test the network. Run **pingall** to test ICMP blocking, or initiate TCP/UDP connections to test port-based filtering

**Logs**:
Blocked packets are logged in the terminal for auditing purposes.


**Contributing**:
Feel free to fork this repository and submit pull requests for enhancements or bug fixes.

**License**:
This project is licensed under the MIT License. See the LICENSE file for details.

