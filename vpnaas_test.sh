#!/usr/bin/env bash

:`this the script to create n east-west vpnaas connections in a single devstack, 
written to analyse the responsetime and cpu overhead
`

EXT_NW_ID=`neutron net-list | awk '/public/{print $2}'`
neutron vpn-ikepolicy-create ikepolicy1
neutron vpn-ipsecpolicy-create ipsecpolicy1
for i in `seq 1 100`;
do    
    WEST_SUBNET_i="192.168."$i".0/24"
    j=$((i+1))
    EAST_SUBNET_i="192.168."$j".0/24"
    function setup_site(){
        local site_name=$1
        local cidr=$2
        neutron net-create net_$site_name
        neutron subnet-create --name subnet_$site_name net_$site_name $2
        neutron router-create router_$site_name
        neutron router-interface-add router_$site_name subnet_$site_name
        neutron router-gateway-set router_$site_name $EXT_NW_ID
        neutron vpn-service-create --name vpn_$site_name router_$site_name subnet_$site_name
    }

    function get_external_ip(){
        local router_id=`neutron router-show $1 | awk '/ id /{print $4}'`
        echo `neutron port-list -c fixed_ips -c device_id -c device_owner|grep router_gateway | awk '/'.$router_id.'/{print $5}' | sed 's/["}]//g'`
    }

    function clean_site(){
        local site_name=$1
        neutron ipsec-site-connection-delete conn_$site_name    
        neutron vpn-service-list | awk '/vpn_'$site_name'/{print "neutron vpn-service-delete " $2}' | bash
        neutron router-gateway-clear router_$site_name
        neutron router-interface-delete router_$site_name subnet_$site_name
        neutron router-list | awk '/router_'$site_name'/{print "neutron router-delete " $2}' | bash
        neutron subnet-list | awk '/subnet_'$site_name'/{print "neutron subnet-delete " $2}' | bash
        neutron net-list | awk '/net_'$site_name'/{print "neutron net-delete " $2}' | bash
     }

    function setup(){
        setup_site west_$i $WEST_SUBNET_i
        WEST_IP=$(get_external_ip router_west_$i)
        setup_site east_$i $EAST_SUBNET_i
        EAST_IP=$(get_external_ip router_east_$i)
        neutron ipsec-site-connection-create --name conn_east_$i --vpnservice-id vpn_east_$i --ikepolicy-id ikepolicy1 --ipsecpolicy-id ipsecpolicy1 --peer-address $WEST_IP --peer-id $WEST_IP --peer-cidr $WEST_SUBNET_i --psk secret
        neutron ipsec-site-connection-create --name conn_west_$i --vpnservice-id vpn_west_$i --ikepolicy-id ikepolicy1 --ipsecpolicy-id ipsecpolicy1 --peer-address $EAST_IP --peer-id $EAST_IP --peer-cidr $EAST_SUBNET_i --psk secret
    }

    function cleanup(){
        clean_site west_$i
        clean_site east_$i
        #neutron vpn-ikepolicy-delete ikepolicy1
        #neutron vpn-ipsecpolicy-delete ipsecpolicy1

    }
    cleanup
    setup



    ((i++))
done

