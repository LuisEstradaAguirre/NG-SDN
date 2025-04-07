# NG-SDN + QoS Project
The Next Generation - Software Defined Networks (NG-SDN) is an open-source platform that implements 3 main technologies:

- [**P4 Programming Language**](https://opennetworking.org/p4/): A domain-specific language for network devices (e.g. switches, routers, NICs) to specify how network data-plane devices process packets.
   
- [**Stratum**](https://opennetworking.org/stratum/): A light open source Operating System designed for network switches used in SDNs.

- [**ONOS**](https://opennetworking.org/onos/): An open sourrce SDN control and configuration platform that manages a network of Stratum-enabled switches.

This projects goal is to implement a QoS solution for the NG-SDN platform.

## What is QoS?
In networking, Quality of Service (QoS) are technologies and techniques used to manage and prioritize network traffic in order to meet specific performance requirements.

QoS ensures that critical or time-sensitive data, such as voice, video, or high-priority applications, receives the necessary bandwidth and experiences minimal delay, packet loss, or jitter.

## Real-World Scenario
Inside a company utilizing an SDN, there's 2 departments: Marketing and Finance.

At the same time when a Marketing Lead is having a video call with a prospect client, the Finance team is having their annual sales meeting; meaning that 10 people is downloading a 3 GB Annual Report file.

On a normal scenario without QoS (which is usually what happens in the real world), the Marketing video call would start lagging and buffering, because the Finance team would be consuming most or all of the available bandwidth.

However, with a QoS solution, even if there's 10 people donlwoading big files, the video call wouldn't suffer because it would prioritize the video call traffic, and still, the other 10 downloads would continue, only at a slower constant rate.

## Project Implementation
This project utilizes 2 Docker containers, one for the ONOS controller, and the other one to simulate an SDN using [**Mininet**](https://mininet.org/) virtualization software. Such Mininet Docker is configured to use the Stratum OS for the virtualized network switches.

## How To Start Setup
NOTE: You will need 3 terminal windows in the qos_implementation directory

First, start the ONOS Docker on Terminal 1
```
make controller
```
Wait for the docker to start, it should take a moment.

Second, start the Mininet + Stratum Docker on Terminal 2
```
make mininet
```

Third, start the Network Configuration on Terminal 3
```
make netcfg
```
After the configuration gets applied, open the ONOS CLI on Terminal 3
```
make cli
```
IMPORTANT: The password is **rocks**

Inside the ONOS shell, type:
```
app activate fwd
```

After that start the QoS Python Test on Terminal 4
```
python test_qos.py
```
