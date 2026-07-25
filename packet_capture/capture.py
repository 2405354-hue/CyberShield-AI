from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

print("Starting packet capturing...")
print("Capturing 5 packets...\n")

sniff(count=5, prn=packet_callback)

print("\nPacket capturing completed.")