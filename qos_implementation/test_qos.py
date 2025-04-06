#!/usr/bin/env python3

import os
import sys
import time
import subprocess
from threading import Thread
from queue import Queue

def setup_qos_tables():
    """Configure QoS tables using P4Runtime shell"""
    print("Setting up QoS tables...")
    # Configure TCP QoS classifier for high priority on port 5001
    cmd = f"../scripts/p4runtime-sh --grpc-addr localhost:50001 --device-id 1 --election-id 0,1"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    commands = """
    # Clear any existing entries first
    try:
        te = table_entry["MyIngress.tcp_qos_classifier"](action="MyIngress.set_priority_high")
        te.match["hdr.tcp.dstPort"] = 5001
        te.delete()
    except:
        pass
    
    try:
        te = table_entry["MyIngress.tcp_qos_classifier"](action="MyIngress.set_priority_low")
        te.match["hdr.tcp.dstPort"] = 5002
        te.delete()
    except:
        pass
    
    try:
        te = table_entry["MyEgress.qos_queuing"](action="MyEgress.set_queue")
        te.match["meta.priority"] = 5
        te.delete()
    except:
        pass
    
    try:
        te = table_entry["MyEgress.qos_queuing"](action="MyEgress.set_queue")
        te.match["meta.priority"] = 0
        te.delete()
    except:
        pass
    
    # Now add the entries
    te = table_entry["MyIngress.tcp_qos_classifier"](action="MyIngress.set_priority_high")
    te.match["hdr.tcp.dstPort"] = 5001
    te.insert()
    
    te = table_entry["MyIngress.tcp_qos_classifier"](action="MyIngress.set_priority_low")
    te.match["hdr.tcp.dstPort"] = 5002
    te.insert()
    
    te = table_entry["MyEgress.qos_queuing"](action="MyEgress.set_queue")
    te.match["meta.priority"] = 5
    te.action["qid"] = 5
    te.insert()
    
    te = table_entry["MyEgress.qos_queuing"](action="MyEgress.set_queue")
    te.match["meta.priority"] = 0
    te.action["qid"] = 0
    te.insert()
    
    # Verify entries
    print("Table entries:")
    print(table_entry["MyIngress.tcp_qos_classifier"].read(lambda te: print(te)))
    print(table_entry["MyEgress.qos_queuing"].read(lambda te: print(te)))
    
    exit()
    """
    stdout, stderr = p.communicate(commands.encode())
    print("QoS tables configured.")
    print("P4Runtime shell output:")
    print(stdout.decode())
    if stderr:
        print("Errors:")
        print(stderr.decode())

def run_iperf_servers():
    """Run iperf servers on h2 for both ports"""
    print("Starting iperf servers on h2...")
    try:
        # Start one server for port 5001 (high priority)
        server_cmd1 = "../scripts/utils/mn-stratum/exec-d-script h2 'iperf -s -p 5001'"
        # Start another server for port 5002 (low priority)
        server_cmd2 = "../scripts/utils/mn-stratum/exec-d-script h2 'iperf -s -p 5002'"
        
        subprocess.run(server_cmd1, shell=True, check=True)
        subprocess.run(server_cmd2, shell=True, check=True)
        print("Iperf servers started on ports 5001 and 5002")
    except subprocess.CalledProcessError as e:
        print(f"Error starting iperf servers: {e}")
    
    time.sleep(2)  # Give servers time to start

def extract_bandwidth(output):
    """Extract bandwidth from iperf output"""
    for line in output.splitlines():
        if "Mbits/sec" in line and "receiver" not in line:
            # Extract the bandwidth value
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "Mbits/sec":
                    try:
                        return float(parts[i-1])
                    except:
                        pass
    return None

def run_iperf_client(host, port, duration=10):
    """Run iperf client and return bandwidth"""
    print(f"Running iperf client on {host} to port {port}...")
    client_cmd = f"../scripts/utils/mn-stratum/exec-script {host} 'iperf -c 10.0.0.2 -t {duration} -p {port}'"
    try:
        output = subprocess.check_output(client_cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        bandwidth = extract_bandwidth(output)
        return bandwidth
    except subprocess.CalledProcessError as e:
        print(f"Error running iperf client: {e.output.decode('utf-8') if hasattr(e, 'output') else str(e)}")
        return None

def run_simultaneous_test(duration=15):
    """Run high and low priority traffic simultaneously and return results"""
    print("\n=== Running simultaneous traffic test ===")
    
    # Use h1 for both tests but with different ports and different temporary files
    try:
        # Start both clients with the same bandwidth demand to see true prioritization
        # Start high priority client in background
        high_cmd = f"../scripts/utils/mn-stratum/exec-d-script h1 'iperf -c 10.0.0.2 -t {duration} -p 5001 -b 50M > /tmp/high_result.txt'"
        subprocess.run(high_cmd, shell=True, check=True)
        
        # Wait a moment
        time.sleep(1)
        
        # Start low priority client in background
        low_cmd = f"../scripts/utils/mn-stratum/exec-d-script h1 'iperf -c 10.0.0.2 -t {duration} -p 5002 -b 50M > /tmp/low_result.txt'"
        subprocess.run(low_cmd, shell=True, check=True)
        
        # Wait for tests to complete
        print(f"Waiting {duration+2} seconds for tests to complete...")
        time.sleep(duration + 2)
        
        # Collect results
        high_result_cmd = "../scripts/utils/mn-stratum/exec-script h1 'cat /tmp/high_result.txt'"
        low_result_cmd = "../scripts/utils/mn-stratum/exec-script h1 'cat /tmp/low_result.txt'"
        
        high_output = subprocess.check_output(high_result_cmd, shell=True).decode('utf-8')
        low_output = subprocess.check_output(low_result_cmd, shell=True).decode('utf-8')
        
        print("\n--- High Priority Output ---")
        print(high_output)
        print("\n--- Low Priority Output ---")
        print(low_output)
        
        high_bw = extract_bandwidth(high_output)
        low_bw = extract_bandwidth(low_output)
            
        return high_bw, low_bw
    
    except Exception as e:
        print(f"Error in simultaneous test: {str(e)}")
        return None, None

def test_qos():
    """Test QoS implementation and show clear results"""
    # Configure QoS tables
    setup_qos_tables()
    
    # Start iperf servers
    run_iperf_servers()
    
    # Test individual performance first
    print("\n=== Testing individual performance ===")
    high_alone = run_iperf_client("h1", 5001)
    # Use h1 for low priority test too
    low_alone = run_iperf_client("h1", 5002)
    
    print(f"\nIndividual performance:")
    print(f"High priority (port 5001): {high_alone:.2f} Mbits/sec" if high_alone else "High priority: Failed to measure")
    print(f"Low priority (port 5002): {low_alone:.2f} Mbits/sec" if low_alone else "Low priority: Failed to measure")
    
    # Test with QoS (competing traffic)
    high_qos, low_qos = run_simultaneous_test()
    
    # Print summary
    print("\n========== QoS TEST RESULTS ==========")
    print("\nIndividual Performance:")
    print(f"High priority (port 5001): {high_alone:.2f} Mbits/sec" if high_alone else "High priority: Failed to measure")
    print(f"Low priority (port 5002): {low_alone:.2f} Mbits/sec" if low_alone else "Low priority: Failed to measure")
    
    print("\nWith QoS (competing traffic):")
    print(f"High priority (port 5001): {high_qos:.2f} Mbits/sec" if high_qos else "High priority: Failed to measure")
    print(f"Low priority (port 5002): {low_qos:.2f} Mbits/sec" if low_qos else "Low priority: Failed to measure")
    
    if high_qos and low_qos:
        ratio = high_qos / low_qos if low_qos > 0 else float('inf')
        print(f"\nHigh/Low priority ratio: {ratio:.2f}x")
        
        if ratio > 1:
            print("\nQoS TEST PASSED: High priority traffic received more bandwidth than low priority traffic")
        else:
            print("\nQoS TEST FAILED: High priority traffic did not receive more bandwidth")
    else:
        print("\nCould not determine QoS effectiveness due to measurement errors")

if __name__ == "__main__":
    test_qos()