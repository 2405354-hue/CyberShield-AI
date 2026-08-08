import pandas as pd
from datetime import datetime

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

    packet_time = datetime.strptime(packet["Time"], "%H:%M:%S")
    
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
        "total_bytes": packet_length,
        "first_time": packet_time,
        "last_time": packet_time
    }
    else:
        flows[flow_key]["packet_count"] += 1
        flows[flow_key]["total_bytes"] += packet_length
        flows[flow_key]["last_time"] = packet_time

print("\nDetected Flows:\n")

for key, value in flows.items():

    duration = (
        value["last_time"] - value["first_time"]
    ).total_seconds()

    if duration > 0:

        packets_per_second = (
            value["packet_count"] / duration
        )

        bytes_per_second = (
            value["total_bytes"] / duration
        )

    else:

        packets_per_second = 0
        bytes_per_second = 0

    average_packet_length = (
        value["total_bytes"] / value["packet_count"]
    )

print("Flow :", key)
print("Packets :", value["packet_count"])
print("Total Bytes :", value["total_bytes"])
print("Flow Duration :", duration, "seconds")
print("Packets/Second :", packets_per_second)
print("Bytes/Second   :", bytes_per_second)
print("Average Packet Length :", average_packet_length)    
print("-" * 50)