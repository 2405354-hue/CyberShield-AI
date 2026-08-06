flows = {}

print("Flow tracker created successfully!")

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