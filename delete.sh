#!/bin/bash

delete_vms() {
  echo "Deleting VMs..."
  nova list --all-tenants | awk 'NR>3 && NF {print $2}' | xargs -I {} nova delete {}
}

delete_s2s_connections() {
  echo "Deleting S2S connections..."
  neutron ipsec-site-connection-list | awk 'NR>3 && NF {print $2}' | xargs -I {} neutron ipsec-site-connection-delete {}
}

delete_ike_policies() {
  echo "Deleting IKE policies..."
  neutron vpn-ikepolicy-list | awk 'NR>3 && NF {print $2}' | xargs -I {} neutron vpn-ikepolicy-delete {}
}

delete_endpoint_groups() {
  echo "Deleting endpoint groups..."
  neutron vpn-endpoint-group-list | awk 'NR>3 && NF {print $2}' | xargs -I {} neutron vpn-endpoint-group-delete {}
}

delete_vpn_services() {
  echo "Deleting VPN services..."
  neutron vpn-service-list | awk 'NR>3 && NF {print $2}' | xargs -I {} neutron vpn-service-delete {}
}

delete_ipsec_policies() {
  echo "Deleting IPsec policies..."
  neutron vpn-ipsecpolicy-list | awk 'NR>3 && NF {print $2}' | xargs -I {} neutron vpn-ipsecpolicy-delete {}
}

delete_images() {
  echo "Deleting images..."
  openstack image list | awk 'NR>3 && NF {print $2}' | xargs -I {} openstack image delete {}
}

delete_routers_and_ports() {
  echo "Deleting routers and router ports..."
  openstack router list | awk '/router_/ {print $2}' | while read -r router; do
    openstack router show "$router" >/dev/null
    if [ $? -eq 0 ]; then
      openstack router delete "$router"
      openstack router show "$router"
      openstack subnet list | awk '/subnet_/ {print $2}' | while read -r subnet; do
        openstack router remove subnet "$router" "$subnet"
        openstack router delete "$router"
      done
    fi
  done
}

delete_networks() {
  echo "Deleting networks..."
  openstack network list | awk '/net/ {print $2}' | xargs -I {} openstack network delete {}
}

echo "Executing cleanup..."
delete_vms
delete_s2s_connections
delete_ike_policies
delete_endpoint_groups
delete_vpn_services
delete_ipsec_policies
delete_images
delete_routers_and_ports
delete_networks

openstack network list
openstack router list
openstack subnet list
openstack router list
openstack image list
neutron vpn-ipsecpolicy-list
neutron vpn-ikepolicy-list
neutron vpn-service-list
neutron vpn-endpoint-group-list
