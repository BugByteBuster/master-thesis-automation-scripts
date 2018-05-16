#!/bin/bash

echo getting token
Token=$(curl -v -s -X POST -H "Content-Type: application/json" -d '{"auth":{"scope": {"project":{"domain": {"name": "Default"}, "name": "admin"}},"identity":{"methods":["password"],"password":{"user":{"name":"admin","password":"s3cr3t","domain":{"name":"Default"}}}}}}' http://10.1.10.146:18090/identity/v3/auth/tokens 2>&1 >/dev/null | grep "Subject-Token" | awk '{print $3}')
echo Token=$Token

echo creating network net1
net1=$(curl -s -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"network": {"name": "net1"}}' http://10.1.10.146:18090/network/v2.0/networks | jq -r .network.id)
echo net1=$net1

echo creating router router_first
extnet_id=$(curl -s -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $Token" http://10.1.10.146:18090/network/v2.0/networks | jq -r '.networks| .[0].id')
router_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"router": {"name": "router_first", "external_gateway_info": {"network_id": "'$extnet_id'"}}}' http://10.1.10.146:18090/router/v2.0/routers | jq -r .router.id)
echo router_id=$router_id

echo creating subnet1
subnet1=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"subnet": {"name": "subnet_1", "network_id": "'$net1'","ip_version": 4,"cidr": "192.168.10.0/24"}}' http://10.1.10.146:18090/network/v2.0/subnets | jq -r .subnet.id)
echo subnet1=$subnet1

echo creating net2
net2=$(curl -s -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"network": {"name": "net2"}}' http://10.1.10.146:18090/network/v2.0/networks | jq -r .network.id)
echo net2=$net2

echo creating subnet2
subnet2=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"subnet": {"name": "subnet_2", "network_id": "'$net2'","ip_version": 4,"cidr": "192.168.20.0/24"}}' http://10.1.10.146:18090/network/v2.0/subnets | jq -r .subnet.id)
echo subnet2=$subnet2

echo creating image
image=$(curl -s -X POST -H "X-Auth-Token:  $Token" -H "Content-Type: application/json" -d '{"name": "cirros1","container_format": "bare","disk_format": "qcow2"}' http://10.1.10.146:18090/image/v2/images | jq -r .id)
echo image_id=$image

echo uploading image
curl -s -X PUT -H "X-Auth-Token: $Token" -H "Content-Type: application/octet-stream" --data-binary @/home/ubuntu/cirros-0.3.4-x86_64-disk.img http://10.1.10.146:18090/image/v2/images/$image/file


echo adding router interface to subnet1
curl -s -X PUT -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"subnet_id": "'$subnet1'"}' http://10.1.10.146:18090/router/v2.0/routers/$router_id/add_router_interface

echo adding router interface to subnet2
curl -s -X PUT -H "Content-Type: application/json" -H "X-Auth-Token: $Token" -d '{"subnet_id": "'$subnet2'"}' http://10.1.10.146:18090/router/v2.0/routers/$router_id/add_router_interface
