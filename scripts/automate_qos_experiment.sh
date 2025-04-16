#!/bin/bash

# 1. Start Mininet topology
# python3 /Users/luisdanielesagui/Desktop/UTEP\ JAN\ -\ MAY\ Semester\ 2025/Computer\ Networks/NG-SDN/scripts/dual_topology.py &

# 2. Wait for Mininet and ONOS to be ready, then install QoS rules
sleep 30  # Adjust as needed for your environment
DEVICE_ID="of:0000000000000002"  # Replace with your actual device ID for the QoS switch
/Users/luisdanielesagui/Desktop/UTEP\ JAN\ -\ MAY\ Semester\ 2025/Computer\ Networks/NG-SDN/scripts/install_qos_rules.sh $DEVICE_ID

# 3. Run traffic generation and measurement
/Users/luisdanielesagui/Desktop/UTEP\ JAN\ -\ MAY\ Semester\ 2025/Computer\ Networks/NG-SDN/scripts/run_traffic.sh