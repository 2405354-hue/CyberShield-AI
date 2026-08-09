import pandas as pd
from datetime import datetime

flows = {}

packets = pd.read_csv("../captured_packets.csv")

for index, packet in packets.iterrows():

    source_ip = packet["Source IP"]
    destination_ip = packet["Destination IP"]
    source_port = packet["Source Port"]
    destination_port = packet["Destination Port"]
    protocol = packet["Protocol"]
    packet_length = packet["Packet Length"]

    packet_time = datetime.strptime(
        packet["Time"],
        "%H:%M:%S"
    )

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

feature_rows = []

for key, value in flows.items():

    duration = (
        value["last_time"] - value["first_time"]
    ).total_seconds()

    if duration > 0:
        packets_per_second = value["packet_count"] / duration
        bytes_per_second = value["total_bytes"] / duration
    else:
        packets_per_second = 0
        bytes_per_second = 0

    average_packet_length = (
        value["total_bytes"] / value["packet_count"]
    )

    feature_rows.append({
        "Packet Count": value["packet_count"],
        "Total Bytes": value["total_bytes"],
        "Flow Duration": duration,
        "Packets Per Second": packets_per_second,
        "Bytes Per Second": bytes_per_second,
        "Average Packet Length": average_packet_length
    })

features = pd.DataFrame(feature_rows)

print("\nFeature Dataset:")
print(features.head())

print("\nFeature Shape:")
print(features.shape)

print("\nFeature Columns:")
print(features.columns)

features.to_csv("../data/flow_extractor.csv",index=False)

print("\nFeature dataset saved successfully!")

print("\nFeature data types:")
print(features.dtypes)

print("\nMissing Values:")
print(features.isnull().sum())