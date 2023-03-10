# Overview

The scripts in this repository demonstrate how to integrate ntcip signalling
functionality with the SIO pipeline.  The setup consists of

* snmp-server: An optional NTCIP/SNMP server component which can serve
as a simulated NTCIP server target when no actual server is available.
* ntcip-relay-server: A component which can convert HTTP requests into
NTCIP server commands using configuration and parameters provided in
an HTTP POST.
* event-webhooks: An SIO pipeline extension which can convert specified
event commands into webhooks.  In this case, we will configure the
extension to generate HTTP POST requests suitable for use with the
ntcip-relay-server (TODO: Not yet implemented)

## Setup

1. Modify the configuration for the services in the respective service `conf` directories, using either the device UI or editing directly via the command line.
* For `ntcip-relay-server.json`, if you wish to use the `snmp-server` container as
the target for NTCIP requests, set your host device or server's IP address in the
`ntcip_controller_ip` field.
* For the `snmp-server` container, customize the `snmp-server.py` field with
the mib(s) you'd like to support/simulate.  For details see the readme at https://github.com/Trellis-Logic/snmp-server

## Running

Start the services using the service start script or device UI.

To test the functionality, use:
```
curl -X POST -F "phase_control_group=1" -F 'phase=1' -F 'signal_type=True' -F "mib=1.3.6.1.4.1.1206.4.2.1.1.5.1.7" http://localhost:8080/pedcall/
```
to send an activation on mib `1.3.6.1.4.1.1206.4.2.1.1.5.1.7`

You should see the corresponding mib set with the query
```
snmpwalk -v2c -c administrator ${deviceip}:501 1.3.6.1.4.1.1206.4.2.1.1.5.1.7
```
Where `${deviceip}` is the IP address of the device running the `snmp-server` container
or the NTCIP server configured in `ntcip_controller_ip` configuration of `ntcip-relay-server.json`
