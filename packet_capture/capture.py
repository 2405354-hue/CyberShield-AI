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

        print("Source IP           :",packet[IP].src)
        print("Destination IP      :",packet[IP].dst)
        print("TTL                 :",packet[IP].ttl)
        print("IP ID               :",packet[IP].id)
        print("Fragement Offset    :",packet[IP].frag)

        protocol = protocols.get(packet[IP].proto, f"Unknown ({packet[IP].proto})")
        print("Protocol            :", protocol)

        if TCP in packet:

            if packet[TCP].dport in services:
                service=services[packet[TCP].dport]
            elif packet[TCP].sport in services:
                service=services[packet[TCP].sport]
            else:
                service= "Unknown"

            flag=packet[TCP].flags
            print(f"TCP Flags           : {flag}")
            
            print(f"Service             : {service}")
            print("Source Port         :", packet[TCP].sport)
            print("Destination Port    :", packet[TCP].dport)

        elif UDP in packet:

            if packet[UDP].dport in services:
                service=services[packet[UDP].dport]
            elif packet[UDP].sport in services:
                service=services[packet[UDP].sport]
            else:
                service= "Unknown"
                        
            print(f"Service             : {service}")            
            print("Source Port         :", packet[UDP].sport)
            print("Destination Port    :", packet[UDP].dport)

        print("Packet length       :", len(packet), "bytes")
        print("_ "*50)
        
print("Capturing 5 packets...\n")

sniff(filter="ip", count=5, prn=packet_callback)

print("\nPacket capturing completed.")