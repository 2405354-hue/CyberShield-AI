import pandas as pd

packets = pd.read_csv("../captured_packets.csv")

print("Captured Packets")

print(packets.head())

print("\nColumns")

print(packets.columns)

print("\nShape")

print(packets.shape)