import pandas as pd

data = pd.read_csv("../captured_packets.csv")

features = data[
    [
        "Ethernet Type",
        "Direction",
        "TTL",
        "IP ID",
        "Fragment Offset",
        "Protocol",
        "Source Port",
        "Destination Port",
        "Service",
        "TCP Flags",
        "Packet Length"
    ]
]

print(features.head())
print(features.shape)
print(features.columns)
print(data.info())
