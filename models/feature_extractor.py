import pandas as pd
from datetime import datetime

flows = {}

def create_flow_key(source_ip, destination_ip,
                    source_port, destination_port, protocol):

    endpoint1 = (
        source_ip,
        source_port
    )

    endpoint2 = (
        destination_ip,
        destination_port
    )

    if endpoint1 <= endpoint2:
        return (
            source_ip,
            source_port,
            destination_ip,
            destination_port,
            protocol
        )
    else:
        return (
            destination_ip,
            destination_port,
            source_ip,
            source_port,
            protocol
        )

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

    flow_key = create_flow_key(
        source_ip,
        destination_ip,
        source_port,
        destination_port,
        protocol
    )
    if flow_key not in flows:

        flows[flow_key] = {
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "source_port": source_port,
            "destination_port": destination_port,

            "packet_count": 1,
            "total_bytes": packet_length,

            "forward_packets": 1,
            "backward_packets": 0,

            "forward_bytes": packet_length,
            "backward_bytes": 0,

            "forward_lengths": [packet_length],
            "backward_lengths": [],

            "forward_times": [packet_time],
            "backward_times": [],

            "first_time": packet_time,
            "last_time": packet_time
        }

    else:

        flows[flow_key]["packet_count"] += 1
        flows[flow_key]["total_bytes"] += packet_length
        flows[flow_key]["last_time"] = packet_time

    if (
        source_ip == flows[flow_key]["source_ip"]
        and source_port == flows[flow_key]["source_port"]
    ):

        flows[flow_key]["forward_packets"] += 1
        flows[flow_key]["forward_bytes"] += packet_length

        flows[flow_key]["forward_lengths"].append(
            packet_length
        )

        flows[flow_key]["forward_times"].append(
            packet_time
        )

    else:

        flows[flow_key]["backward_packets"] += 1
        flows[flow_key]["backward_bytes"] += packet_length

        flows[flow_key]["backward_lengths"].append(
            packet_length
        )

        flows[flow_key]["backward_times"].append(
            packet_time
        )

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

    forward_lengths = value["forward_lengths"]
    backward_lengths = value["backward_lengths"]

    fwd_max = max(forward_lengths)
    fwd_min = min(forward_lengths)
    fwd_mean = sum(forward_lengths) / len(forward_lengths)

    if len(forward_lengths) > 1:
        fwd_std = pd.Series(forward_lengths).std()
    else:
        fwd_std = 0

    if backward_lengths:
        bwd_max = max(backward_lengths)
        bwd_min = min(backward_lengths)
        bwd_mean = sum(backward_lengths) / len(backward_lengths)

        if len(backward_lengths) > 1:
            bwd_std = pd.Series(backward_lengths).std()
        else:
            bwd_std = 0

    else:
        bwd_max = 0
        bwd_min = 0
        bwd_mean = 0
        bwd_std = 0

    feature_rows.append({
    "Destination Port": value["destination_port"],
    "Flow Duration": duration * 1_000_000,

    "Total Fwd Packets": value["forward_packets"],
    "Total Length of Fwd Packets": value["forward_bytes"],

    "Fwd Packet Length Max": fwd_max,
    "Fwd Packet Length Min": fwd_min,
    "Fwd Packet Length Mean": fwd_mean,
    "Fwd Packet Length Std": fwd_std,

    "Bwd Packet Length Max": bwd_max,
    "Bwd Packet Length Min": bwd_min,
    "Bwd Packet Length Mean": bwd_mean,
    "Bwd Packet Length Std": bwd_std
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