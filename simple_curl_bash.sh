#!/bin/bash

get_token() {
  local token=$(curl -v -s -X POST -H "Content-Type: application/json" -d '{"auth":{"scope": {"project":{"domain": {"name": "Default"}, "name": "admin"}},"identity":{"methods":["password"],"password":{"user":{"name":"admin","password":"s3cr3t","domain":{"name":"Default"}}}}}}' http://10.1.10.146:18090/identity/v3/auth/tokens 2>&1 >/dev/null | grep "Subject-Token" | awk '{print $3}')
  echo "Token=$token"
}

create_network() {
  local network_name=$1
  local token=$2
  local network_id=$(curl -s -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"network": {"name": "'$network_name'"}}' http://10.1.10.146:18090/network/v2.0/networks | jq -r .network.id)
  echo "$network_name=$network_id"
}

create_router() {
  local router_name=$1
  local token=$2
  local extnet_id=$(curl -s -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $token" http://10.1.10.146:18090/network/v2.0/networks | jq -r '.networks| .[0].id')
  local router_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"router": {"name": "'$router_name'", "external_gateway_info": {"network_id": "'$extnet_id'"}}}' http://10.1.10.146:18090/router/v2.0/routers | jq -r .router.id)
  echo "router_id=$router_id"
}

create_subnet() {
  local subnet_name=$1
  local network_id=$2
  local token=$3
  local subnet_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"subnet": {"name": "'$subnet_name'", "network_id": "'$network_id'","ip_version": 4,"cidr": "192.168.'$subnet_name'.0/24"}}' http://10.1.10.146:18090/network/v2.0/subnets | jq -r .subnet.id)
  echo "$subnet_name=$subnet_id"
}

upload_image() {
  local image_name=$1
  local token=$2
  local image_id=$(curl -s -X POST -H "X-Auth-Token: $token" -H "Content-Type: application/json" -d '{"name": "'$image_name'","container_format": "bare","disk_format": "qcow2"}' http://10.1.10.146:18090/image/v2/images | jq -r .id)
  echo "image_id=$image_id"
  curl -s -X PUT -H "X-Auth-Token: $token" -H "Content-Type: application/octet-stream" --data-binary @/home/ubuntu/cirros-0.3.4-x86_64-disk.img http://10.1.10.146:18090/image/v2/images/$image_id/file
}

add_router_interface() {
  local router_id=$1
  local subnet_id=$2
  local token=$3
  curl -s -X PUT -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"subnet_id": "'$subnet_id'"}' http://10.1.10.146:18090/router/v2.0/routers/$router_id/add_router_interface
}

# Main script

echo "Getting token"
token=$(get_token)

echo "Creating network net1"
net1=$(create_network "net1" "$token")

echo "Creating router router_first"
router_first=$(create_router "router_first" "$token")

echo "Creating subnet1"
subnet1=$(create_subnet "subnet_1" "$net1" "$token")

echo "Creating network net2"
net2=$(create_network "net2" "$token")

echo "Creating subnet2"
subnet2=$(create_subnet "subnet_2" "$net2" "$token")

echo "Creating image"
image=$(upload_image "cirros1" "$token")

echo "Adding router interface to subnet1"
add_router_interface "$router_first" "$subnet1" "$token"

echo "Adding router interface to subnet2"
add_router_interface "$router_first" "$subnet2" "$token"
