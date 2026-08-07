import pandas as pd

flows = {}

packets = pd.read_csv("../captured_packets.csv")

print(packets.head())

for index, packet in packets.iterrows():
    source_ip = packet["Source IP"]
    destination_ip = packet["Destination IP"]
    source_port = packet["Source Port"]
    destination_port = packet["Destination Port"]
    protocol = packet["Protocol"]
    packet_length = packet["Packet Length"]#used to claculate the stastics of flows

    flow_key = (
        source_ip,
        destination_ip,
        source_port,
        destination_port,
        protocol
    )

    if flow_key not in flows:
        flows[flow_key] = {
            "packet_count": 1,
            "total_bytes": packet_length
        }
    else:
        flows[flow_key]["packet_count"] += 1
        flows[flow_key]["total_bytes"] += packet_length

print("\nDetected Flows:\n")

for key, value in flows.items():

    print("Flow           :", key)
    print("Packets        :", value["packet_count"])
    print("Total Bytes    :", value["total_bytes"])
    print("-" * 50)