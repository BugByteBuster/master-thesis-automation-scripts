#!/bin/bash

controller_ip=$1
echo $controller_ip
echo getting token
Token=$(curl -v -s -X POST -H "Content-Type: application/json" -d '{"auth":{"scope": {"project":{"domain": {"name": "Default"}, "name": "admin"}},"identity":{"methods":["password"],"password":{"user":{"name":"admin","password":"s3cr3t","domain":{"name":"Default"}}}}}}' http://$controller_ip:18090/identity/v3/auth/tokens 2>&1 >/dev/null | grep "Subject-Token" | awk '{print $3}')
echo Token=$Token




echo creating router router_first
extnet_id=$(curl -s -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $Token" http://$controller_ip:18090/network/v2.0/networks | jq -r '.networks| .[0].id')
router_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"router": {"name": "router_first", "external_gateway_info": {"network_id": "'$extnet_id'"}}}' $controller_ip:18090/router/v2.0/routers | jq -r .router.id)
echo router_id=$router_id


for net in `seq 1 15`;
do
   network_id=$(curl -s -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"network": {"name": "net$net"}}' http://10.1.10.146:18090/network/v2.0/networks | jq -r .network.id)

   subnet_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"subnet": {"name": "subnet_1", "network_id": "'$network_id'","ip_version": 4,"cidr": "192.168.$net.0/24"}}' http://$controller_ip:18090/network/v2.0/subnets | jq -r .subnet.id)
done

