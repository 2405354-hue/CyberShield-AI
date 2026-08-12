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

    if protocol == "TCP":
        header_length = 40

    elif protocol == "UDP":
        header_length = 28

    else:
        header_length = 20

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

            "forward_header_length": header_length,
            "backward_header_length": 0,

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
        flows[flow_key]["forward_header_length"] += header_length

        flows[flow_key]["forward_lengths"].append(
            packet_length
        )

        flows[flow_key]["forward_times"].append(
            packet_time
        )

    else:

        flows[flow_key]["backward_packets"] += 1
        flows[flow_key]["backward_bytes"] += packet_length
        flows[flow_key]["backward_header_length"] += header_length

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

        fwd_packets_per_second = (
            value["forward_packets"] / duration
        )

        bwd_packets_per_second = (
            value["backward_packets"] / duration
        )

    else:

        fwd_packets_per_second = 0
        bwd_packets_per_second = 0

    if duration > 0:

        flow_bytes_per_second = (
        value["total_bytes"] / duration
        )

        flow_packets_per_second = (
        value["packet_count"] / duration
        )

    else:

        flow_bytes_per_second = 0
        flow_packets_per_second = 0

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

all_times = (
    value["forward_times"]
    + value["backward_times"]
)

all_times.sort()

iat_values = []

for i in range(1, len(all_times)):

    iat = (
        all_times[i] - all_times[i - 1]
    ).total_seconds()

    iat_values.append(iat)

    if iat_values:

        flow_iat_mean = sum(iat_values) / len(iat_values)

        flow_iat_max = max(iat_values)
        flow_iat_min = min(iat_values)

        if len(iat_values) > 1:
            flow_iat_std = pd.Series(iat_values).std()
        else:
            flow_iat_std = 0

    else:

        flow_iat_mean = 0
        flow_iat_std = 0
        flow_iat_max = 0
        flow_iat_min = 0

forward_times = sorted(value["forward_times"])

fwd_iat_values = []

for i in range(1, len(forward_times)):

    iat = (
        forward_times[i] - forward_times[i - 1]
    ).total_seconds()

    fwd_iat_values.append(iat)

if fwd_iat_values:

    fwd_iat_total = sum(fwd_iat_values)
    fwd_iat_mean = fwd_iat_total / len(fwd_iat_values)
    fwd_iat_max = max(fwd_iat_values)
    fwd_iat_min = min(fwd_iat_values)

    if len(fwd_iat_values) > 1:
        fwd_iat_std = pd.Series(fwd_iat_values).std()
    else:
        fwd_iat_std = 0

else:

    fwd_iat_total = 0
    fwd_iat_mean = 0
    fwd_iat_std = 0
    fwd_iat_max = 0
    fwd_iat_min = 0

backward_times = sorted(value["backward_times"])

bwd_iat_values = []

for i in range(1, len(backward_times)):

    iat = (
        backward_times[i] - backward_times[i - 1]
    ).total_seconds()

    bwd_iat_values.append(iat)

if bwd_iat_values:

    bwd_iat_total = sum(bwd_iat_values)
    bwd_iat_mean = bwd_iat_total / len(bwd_iat_values)
    bwd_iat_max = max(bwd_iat_values)
    bwd_iat_min = min(bwd_iat_values)

    if len(bwd_iat_values) > 1:
        bwd_iat_std = pd.Series(bwd_iat_values).std()
    else:
        bwd_iat_std = 0

else:

    bwd_iat_total = 0
    bwd_iat_mean = 0
    bwd_iat_std = 0
    bwd_iat_max = 0
    bwd_iat_min = 0

all_packet_lengths = (
    value["forward_lengths"]
    + value["backward_lengths"]
)

packet_min = min(all_packet_lengths)
packet_max = max(all_packet_lengths)
packet_mean = (
    sum(all_packet_lengths) / len(all_packet_lengths)
)

if len(all_packet_lengths) > 1:
    packet_std = pd.Series(all_packet_lengths).std()
    packet_variance = pd.Series(all_packet_lengths).var()
else:
    packet_std = 0
    packet_variance = 0

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
    "Bwd Packet Length Std": bwd_std,

    "Flow Bytes/s": flow_bytes_per_second,
    "Flow Packets/s": flow_packets_per_second,
    "Flow IAT Mean": flow_iat_mean,
    "Flow IAT Std": flow_iat_std,
    "Flow IAT Max": flow_iat_max,
    "Flow IAT Min": flow_iat_min,

    "Fwd IAT Total": fwd_iat_total * 1_000_000,
    "Fwd IAT Mean": fwd_iat_mean * 1_000_000,
    "Fwd IAT Std": fwd_iat_std * 1_000_000,
    "Fwd IAT Max": fwd_iat_max * 1_000_000,
    "Fwd IAT Min": fwd_iat_min * 1_000_000,

    "Bwd IAT Total": bwd_iat_total * 1_000_000,
    "Bwd IAT Mean": bwd_iat_mean * 1_000_000,
    "Bwd IAT Std": bwd_iat_std * 1_000_000,
    "Bwd IAT Max": bwd_iat_max * 1_000_000,
    "Bwd IAT Min": bwd_iat_min * 1_000_000,

    "Fwd Header Length": value["forward_header_length"],
    "Bwd Header Length": value["backward_header_length"],

    "Fwd Packets/s": fwd_packets_per_second,
    "Bwd Packets/s": bwd_packets_per_second,

    "Min Packet Length": packet_min,
    "Max Packet Length": packet_max,
    "Packet Length Mean": packet_mean,
    "Packet Length Std": packet_std,
    "Packet Length Variance": packet_variance,
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