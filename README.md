this is the code to interact with Openstack..

code.py does the following steps

1. creates network..
2. Creates subnet..
3. launches an instance
4. creates the router and adds interfaces tothe public and prvate network
5. creates ike policy 
6. creates ipsec policy 
6. creates a vpn on the router created



vpnaas_test.sh is the script to deploy n networks, n routers, n vpn services,
1 IKEpolicy and 1 IPsec policy.

the same ike and ipsec policy is used for all the vpn services
it creates n east to west connections within the single devstack
