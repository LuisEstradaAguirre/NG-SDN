#!/bin/bash

# Example: Start iperf servers on all hosts (run in Mininet CLI or via script)
xterm h1a -e "iperf -s -u -p 5001" &
xterm h1b -e "iperf -s -p 5002" &
xterm h1c -e "iperf -s -p 5003" &
xterm h2a -e "iperf -s -u -p 5001" &
xterm h2b -e "iperf -s -p 5002" &
xterm h2c -e "iperf -s -p 5003" &

# Start UDP video call (simulate 2 Mbps video)
xterm h1a -e "iperf -c h1b -u -b 2M -t 60 -p 5001 > h1a_udp.log" &
xterm h2a -e "iperf -c h2b -u -b 2M -t 60 -p 5001 > h2a_udp.log" &

# Start TCP file downloads
xterm h1c -e "iperf -c h1b -t 60 -p 5002 > h1c_tcp.log" &
xterm h2c -e "iperf -c h2b -t 60 -p 5002 > h2c_tcp.log" &