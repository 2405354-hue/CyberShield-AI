import csv

from socket import gethostbyname,gethostname

local_ip=gethostbyname(gethostname())

from datetime import datetime

from scapy.all import *

packet_number=0

services = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    161: "SNMP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8009: "AJP",
    8080: "HTTP-Alt"
}

protocols = {
    1: "ICMP",
    2: "IGMP",
    4: "IPIP",
    6: "TCP",
    8: "EGP",
    17: "UDP",
    41: "IPv6",
    43: "IPv6-Route",
    44: "IPv6-Frag",
    46: "RSVP",
    47: "GRE",
    50: "ESP",
    51: "AH",
    58: "ICMPv6",
    59: "No Next Header",
    60: "IPv6-Opts",
    88: "EIGRP",
    89: "OSPF",
    94: "IPIP",
    103: "PIM",
    112: "VRRP",
    115: "L2TP",
    132: "SCTP",
    136: "UDP-Lite",
    137: "MPLS",
    139: "HIP",
    140: "Shim6"
}

csv_file = "captured_packets.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Packet No",
        "Time",
        "Source MAC",
        "Destination MAC",
        "Ethernet Type",
        "Direction",
        "Source IP",
        "Destination IP",
        "TTL",
        "IP ID",
        "Fragment Offset",
        "Protocol",
        "Source Port",
        "Destination Port",
        "Service",
        "TCP Flags",
        "Packet Length"
    ])

def packet_callback(packet):

    if IP not in packet:
        return

    global packet_number
    packet_number+=1

    current_time=datetime.now().strftime("%H:%M:%S")

    print("="*50)
    print(f"packet #{packet_number}")
    print("="*50)

    print(f"Time                : {current_time}")

    if IP in packet:

        if packet[IP].src == local_ip:
                direction="Outgoing"
        elif packet[IP].dst == local_ip:
                direction="Incoming"
        else:
                direction="Unknown"

        print(f"Direction           : {direction}")

        source_ip = packet[IP].src
        print("Source IP           :", source_ip)

        destination_ip = packet[IP].dst
        print("Destination IP      :", destination_ip)

        ttl = packet[IP].ttl
        print("TTL                 :", ttl)

        ip_id = packet[IP].id
        print("IP ID               :", ip_id)

        fragment_offset = packet[IP].frag
        print("Fragment Offset     :", fragment_offset)
        
        packet_length = len(packet)
        
        protocol = protocols.get(packet[IP].proto, f"Unknown ({packet[IP].proto})")
        print("Protocol            :", protocol)

        source_port = ""
        destination_port = ""
        service = ""
        flag = ""

        if TCP in packet:

            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

            if packet[TCP].dport in services:
                service=services[destination_port]
            elif packet[TCP].sport in services:
                service=services[source_port]
            else:
                service= "Unknown"

            flag= str(packet[TCP].flags)
            print(f"TCP Flags           : {flag}")

            print(f"Service             : {service}")
            print("Source Port         :", source_port)
            print("Destination Port    :", destination_port)

        elif UDP in packet:

            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

            if packet[UDP].dport in services:
                service=services[destination_port]
            elif packet[UDP].sport in services:
                service=services[source_port]
            else:
                service= "Unknown"

            print(f"Service             : {service}")            
            print("Source Port         :", source_port)
            print("Destination Port    :", destination_port)
                
        source_mac = ""
        destination_mac = ""
        ethernet_type = ""

        if Ether in packet:

            source_mac = packet[Ether].src
            destination_mac = packet[Ether].dst

            print("Source MAC          :", source_mac)
            print("Destination MAC     :", destination_mac)

            ethernet_type = hex(packet[Ether].type)
            print("Ethernet Type       :", ethernet_type)

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                packet_number,
                current_time,
                source_mac,
                destination_mac,
                ethernet_type,
                direction,
                source_ip,
                destination_ip,
                ttl,
                ip_id,
                fragment_offset,
                protocol,
                source_port,
                destination_port,
                service,
                flag,
                packet_length
            ])
                        
        print("Packet length       :", packet_length , "bytes")
        print("_ "*50)
        
print("Capturing 5 packets...\n")

sniff(filter="ip", count=100, prn=packet_callback)

print("\nPacket capturing completed.")