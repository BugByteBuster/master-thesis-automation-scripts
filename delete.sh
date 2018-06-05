#!/bin/bash

openstack router list
nova list --all-tenants

#deleting vm
for vm in $(nova list --all-tenants | tail -n +4 | head -n -1 | awk '{print$2}')
do
    nova delete $vm
done

#deleting s2s connection
for s2s in $(neutron ipsec-site-connection-list | tail -n+4 | head -n -1 |awk '{print $2}')
do
neutron ipsec-site-connection-delete $s2s
done

#deleting ike
for ike in $(neutron vpn-ikepolicy-list | tail -n +4 | head -n -1 | awk '{print $2}')
do
neutron vpn-ikepolicy-delete $ike 
done

#deleting endpoint group
for endpoint in $(neutron vpn-endpoint-group-list | tail -n +4 | head -n -1 | awk '{print $2}')
do
neutron vpn-endpoint-group-delete $endpoint 
done

#deleting vpnservice
for service in $(neutron vpn-service-list | tail -n +4 | head -n -1 | awk '{print $2}')
do
neutron vpn-service-delete $service 
done


#deleting isec
for ipsec in $(neutron vpn-ipsecpolicy-list | tail -n +4 | head -n -1 | awk '{print $2}')
do
neutron vpn-ipsecpolicy-delete $ipsec 
done

#deleting image
for image in $(openstack image list | tail -n +4 | head -n -1 | awk '{print $2}')
do 
    openstack image delete $image
done


#deleting router and router ports
for router in $(openstack router list | grep -w "router_" | awk '{print $2}')
do
    openstack router delete $router
    openstack router show $router
    for subnet in $(openstack subnet list | grep  "subnet_" | awk '{print $2}')
    do
        openstack router remove subnet $router $subnet
        openstack router delete $router
    done
done


#deleting network
for network in $(openstack network list | tail -n +4 |head -n -1 | grep "net" | awk '{print$2}')
do
   openstack network delete $network
done



openstack network list
openstack router list
openstack subnet list
openstack router list
openstack image list
neutron vpn-ipsecpolicy-list
neutron vpn-ikepolicy-list
neutron vpn-service-list 
neutron vpn-endpoint-group-list
