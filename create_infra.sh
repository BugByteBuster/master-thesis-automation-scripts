#!/bin/bash

controller_ip=$1
echo $controller_ip

get_token() {
  local token=$(curl -v -s -X POST -H "Content-Type: application/json" -d '{"auth":{"scope": {"project":{"domain": {"name": "Default"}, "name": "admin"}},"identity":{"methods":["password"],"password":{"user":{"name":"admin","password":"s3cr3t","domain":{"name":"Default"}}}}}}' "http://$controller_ip:18090/identity/v3/auth/tokens" 2>&1 >/dev/null | grep "Subject-Token" | awk '{print $3}')
  echo $token
}

echo getting token
Token=$(get_token)
echo $Token

create_router() {
  local token=$1
  local controller_ip=$2

  echo creating router router_first
  extnet_id=$(curl -s -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $token" "http://${controller_ip}:18090/network/v2.0/networks" | jq -r '.networks | .[0].id')
  echo $extnet_id
  router_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"router": {"name": "router_first", "external_gateway_info": {"network_id": "'$extnet_id'"}}}' "${controller_ip}:18090/router/v2.0/routers" | jq -r .router.id)
  #extnet_id=$(curl -s -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $token" "http://${controller_ip}:18090/network/v2.0/networks" | jq -r '.networks | .[] | select(.name=="public") | .id')
  echo router_id=$router_id
}

create_image() {
  local token=$1
  local controller_ip=$2

  echo creating image
  image=$(curl -s -X POST -H "X-Auth-Token: $token" -H "Content-Type: application/json" -d '{"name": "cirros1","container_format": "bare","disk_format": "qcow2"}' "http://${controller_ip}:18090/image/v2/images" | jq -r .id)
  echo image_id=$image

  echo uploading image
  curl -s -X PUT -H "X-Auth-Token: $token" -H "Content-Type: application/octet-stream" --data-binary @/home/ubuntu/cirros-0.3.4-x86_64-disk.img "http://${controller_ip}:18090/image/v2/images/$image/file"
}

create_network_subnet_instance() {
  local token=$1
  local controller_ip=$2

  for net in $(seq 158 172); do
    echo creating network
    network_id=$(curl -s -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"network": {"name": "net'$net'"}}' "http://${controller_ip}:18090/network/v2.0/networks" | jq -r .network.id)
    echo $network_id

    echo creating subnet
    subnet_id=$(curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"subnet": {"name": "subnet_'$net'", "network_id": "'$network_id'","ip_version": 4,"cidr": "192.168.'$net'.0/24"}}' "http://${controller_ip}:18090/network/v2.0/subnets" | jq -r .subnet.id)
    echo $subnet_id

    echo creating instance
    curl -s -X POST -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"server": {"name": "test1","imageRef": "'$image'","flavorRef": "1","networks": [{"uuid": "'$network_id'"}]}}' "http://${controller_ip}:18090/compute/v2.1/servers?sp-10.2.10.$net"

    echo adding interface to router
    port_id=$(curl -s -X PUT -H "Content-Type: application/json" -H "X-Auth-Token: $token" -d '{"subnet_id": "'$subnet_id'"}' "http://${controller_ip}:18090/router/v2.0/routers/$router_id/add_router_interface" | jq -r .port_id)
    echo $port_id
  done
}

create_router $Token $controller_ip
create_image $Token $controller_ip
create_network_subnet_instance $Token $controller_ip
