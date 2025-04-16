#!/bin/bash

ONOS_USER=onos
ONOS_PASS=rocks
ONOS_IP=localhost
DEVICE_ID=$1  # Pass the device ID as the first argument

# Set high priority for UDP port 5001 (video call)
curl -u $ONOS_USER:$ONOS_PASS -X POST -H "Content-Type: application/json" \
  http://$ONOS_IP:8181/onos/v1/flows/$DEVICE_ID \
  -d '{
    "priority": 40000,
    "isPermanent": true,
    "tableId": 1,
    "selector": {
      "criteria": [
        { "type": "ETH_TYPE", "ethType": "0x0800" },
        { "type": "IP_PROTO", "protocol": 17 },
        { "type": "UDP_DST", "udpPort": 5001 }
      ]
    },
    "treatment": {
      "instructions": [
        { "type": "EXTENSION", "extension": { "set_priority_high": {} } }
      ]
    }
  }'

# Set low priority for TCP (file download)
curl -u $ONOS_USER:$ONOS_PASS -X POST -H "Content-Type: application/json" \
  http://$ONOS_IP:8181/onos/v1/flows/$DEVICE_ID \
  -d '{
    "priority": 40000,
    "isPermanent": true,
    "tableId": 2,
    "selector": {
      "criteria": [
        { "type": "ETH_TYPE", "ethType": "0x0800" },
        { "type": "IP_PROTO", "protocol": 6 }
      ]
    },
    "treatment": {
      "instructions": [
        { "type": "EXTENSION", "extension": { "set_priority_low": {} } }
      ]
    }
  }'