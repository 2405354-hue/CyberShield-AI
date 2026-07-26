from scapy.all import *

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

    if IP in packet:

        print("Source IP           :",packet[IP].src)
        print("Destination IP      :",packet[IP].dst)

        protocol = protocols.get(packet[IP].proto, f"Unknown ({packet[IP].proto})")
        print("Protocol            :", protocol)

        if TCP in packet:

            print("Source Port         :", packet[TCP].sport)
            print("Destination Port    :", packet[TCP].dport)

        elif UDP in packet:

            print("Source Port         :", packet[UDP].sport)
            print("Destination Port    :", packet[UDP].dport)

        print("Packet length       :", len(packet), "bytes")
        print("_ "*50)
        
print("Capturing 5 packets...\n")

sniff(count=5, prn=packet_callback)

print("\nPacket capturing completed.")