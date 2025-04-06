# QoS Implementation for NG-SDN

This project implements Quality of Service (QoS) using P4 on the NG-SDN platform (ONOS, Stratum, and P4). The implementation prioritizes traffic based on TCP/UDP port numbers and applies different queuing strategies to provide better service to high-priority traffic.

## Project Structure

- `p4src/qos.p4`: P4 program implementing QoS functionality
- `cfg/netcfg.json`: Network configuration for ONOS
- `test_qos.py`: Python script to test QoS implementation
- `Makefile`: Simplifies building and running the project

## How It Works

The QoS implementation works as follows:

1. **Traffic Classification**: Packets are classified based on TCP/UDP port numbers into high, medium, and low priority.
2. **DSCP Marking**: The Differentiated Services Code Point (DSCP) field in the IP header is set according to the priority.
3. **Queue Assignment**: Packets are assigned to different queues based on their priority.
4. **Forwarding**: Packets are forwarded according to the routing table.

## Setup and Running

### 1. Build the P4 Program

```bash
cd public/assignments/qos_implementation
make build