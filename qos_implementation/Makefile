# Makefile for QoS implementation

P4C = ../scripts/p4c
ONOS = ../scripts/onos
ONOS_CLI = ../scripts/onos-cli
ONOS_APP = ../scripts/onos-app
ONOS_NETCFG = ../scripts/onos-netcfg
MN_STRATUM = ../scripts/mn-stratum
P4RUNTIME_SH = ../scripts/p4runtime-sh
EXEC_SCRIPT = ../scripts/utils/mn-stratum/exec-script
EXEC_D_SCRIPT = ../scripts/utils/mn-stratum/exec-d-script
EXEC = ../scripts/utils/mn-stratum/exec

# P4 source files
P4_SRC = p4src/qos.p4
P4_BUILD_DIR = p4build
BMV2_JSON = $(P4_BUILD_DIR)/qos.json
P4INFO = $(P4_BUILD_DIR)/qos.p4info.txt

# Mininet topology
TOPO = topology.py

# Default target
all: build

# Build P4 program
build: $(BMV2_JSON) $(P4INFO)

$(P4_BUILD_DIR):
	mkdir -p $(P4_BUILD_DIR)

$(BMV2_JSON) $(P4INFO): $(P4_SRC) | $(P4_BUILD_DIR)
	docker run --rm -v $(PWD):/workdir -w /workdir opennetworking/p4c:stable \
		p4c-bm2-ss --arch v1model \
		--p4runtime-files $(P4INFO) \
		--p4runtime-format text \
		$(P4_SRC) -o $(BMV2_JSON)

# Start ONOS controller
controller:
	ONOS_APPS=gui,proxyarp,hostprovider,lldpprovider,drivers.bmv2 $(ONOS)

# Start Mininet with Stratum
mininet:
	$(MN_STRATUM)

# Start ONOS CLI
cli:
	$(ONOS_CLI)

# Configure ONOS with our network configuration
netcfg:
	$(ONOS_NETCFG) cfg/netcfg.json

# Access host h1
host-h1:
	$(EXEC) h1

# Access host h2
host-h2:
	$(EXEC) h2

# Run iperf server on h2
iperf-server:
	$(EXEC_SCRIPT) h2 "iperf -s"

# Run iperf client on h1 with QoS
iperf-client-qos:
	$(EXEC_SCRIPT) h1 "iperf -c 10.0.0.2 -t 30 -p 5001"

# Run iperf client on h1 without QoS
iperf-client-no-qos:
	$(EXEC_SCRIPT) h1 "iperf -c 10.0.0.2 -t 30 -p 5002"

# Build and install the QoS pipeline as an ONOS app
install-pipeline: $(BMV2_JSON) $(P4INFO)
	# Use a simpler approach with ONOS CLI
	$(ONOS_CLI) app:install! $(PWD)/$(P4INFO) $(PWD)/$(BMV2_JSON)
	# Configure QoS tables
	$(ONOS_CLI) "cfg set org.onosproject.net.flow.impl.FlowRuleManager allowExtraneousRules true"
	$(ONOS_CLI) "cfg set org.onosproject.net.flow.impl.FlowRuleManager allowDuplicateFlows true"
	# Create a pipeconf JSON file
	echo '{"pipeconf":{"id":"org.onosproject.pipelines.qos","name":"QoS Pipeline","description":"P4 pipeline with QoS support","p4info":"'$(PWD)/$(P4INFO)'","bmv2json":"'$(PWD)/$(BMV2_JSON)'","type":"bmv2"}}' > $(P4_BUILD_DIR)/pipeconf.json
	# Install the pipeconf using the REST API
	curl -X POST -H "Content-Type: application/json" -d @$(P4_BUILD_DIR)/pipeconf.json http://localhost:8181/onos/v1/pipeconf
	rm -rf app-simple
	mkdir -p app-simple/app/org.onosproject.pipelines.qos/1.0.0/p4c-out/
	cp $(BMV2_JSON) app-simple/app/org.onosproject.pipelines.qos/1.0.0/p4c-out/
	cp $(P4INFO) app-simple/app/org.onosproject.pipelines.qos/1.0.0/p4c-out/
	echo '{"priority":-10,"apps":{"org.onosproject.pipelines.qos":{"pipeconf":{"p4info":"p4c-out/qos.p4info.txt","bmv2json":"p4c-out/qos.json","type":"bmv2"}}}}' > app-simple/app/org.onosproject.pipelines.qos/1.0.0/app.json
	cd app-simple && zip -r qos-pipeline.oar app
	$(ONOS_APP) install! app-simple/qos-pipeline.oar

# Clean build artifacts
clean:
	rm -rf $(P4_BUILD_DIR)

.PHONY: all build controller mininet cli netcfg host-h1 host-h2 iperf-server iperf-client-qos iperf-client-no-qos install-pipeline clean