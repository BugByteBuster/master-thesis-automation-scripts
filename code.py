import sys
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
url= "http://"+sys.argv[1]+"/identity/v3"
auth = v3.Password(auth_url=url, username="admin",
                   password="password", project_name="demopro1",
                   user_domain_id="default", project_domain_id="default")
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)
if sys.argv[1]=='192.168.2.7':
    cidr = "192.168.2.0/24"
elif sys.argv[1]== '192.168.2.8':
     cidr = "192.168.3.0/24"
elif sys.argv[1]=='192.168.2.9':
     cidr = "192.168.4.0/24"
#Glance
from glanceclient.v2 import Client
glance = Client(session=sess)
available_images=[]
for image in glance.images.list():
    available_images.append(image.id)
boot_image=available_images[0]
#Neutron
from neutronclient.v2_0 import client
neutron = client.Client(session=sess)
subnets = neutron.list_subnets()
print "creating network....."
networks=neutron.list_networks(name='public')
external_netid=networks['networks'][0]['id'] 
net=neutron.create_network(
                               body={
                                "network": {
                                   "name": "net1",
                                   "admin_state_up": True
                                          }
                                     }
                                )

boot_net = net['network']['id']
print "creating subnet......"
subnet=neutron.create_subnet(
                                 body={
                                  "subnet": {
                                    "name":"subnet1",
                                    "network_id": boot_net,
                                    "ip_version": 4,
                                    "cidr": cidr
                                             }
                                        }
                                   )

boot_subnet = subnet['subnet']['id']


#Nova
from novaclient import client
nova = client.Client('2.1', session=sess)
boot_flav= nova.flavors.find(name='m1.nano')
print "booting instance...."
instance_boot=nova.servers.create(name="instance1", image=boot_image, flavor=boot_flav, network=boot_subnet)
#creating router
print "Creating the router and adding the interfaces......"
router=neutron.create_router(
                             body={
                                     "router": {
                                         "name": "router1",
                                         "external_gateway_info": {
                                             "network_id": external_netid,
                                             "enable_snat": True
                                                                    },
                                      "admin_state_up": True,
                                               }
                                    }                             
)

router_id=router['router']['id']
neutron.add_interface_router(router_id, 
                             body={
                                   "subnet_id":boot_subnet 
                                  }
                             )


#creating vpn service
print "Setting UP VPN"

print "1.Creating IKE Policy..."

neutron.create_ikepolicy(
                             body={
                                   "ikepolicy" : {
                                        "name": "ikepolicy_1",
                                        "auth_algorithm" : "sha1",
                                        "encryption_algorithm" : "aes-256",
                                        "phase1_negotiation_mode" : "main"
                                        #"lifetime_unit" : "seconds",
                                        #"lifetime_value" : "28800",
                                        #"pfs": " Group5"
                                                    }
                                   }
                             )


print "2.Creating IPSEC Policy ......"

neutron.create_ipsecpolicy(
                           body={
  "ipsecpolicy" : {
            "name": "ipsecpolicy_1",
            "transform_protocol": "esp",
	    "auth_algorithm" : "sha1",
            "encryption_algorithm" : "aes-256",
            "encapsulation_mode" : "tunnel"
            #"lifetime_units" : "seconds",
            #"lifetime_value" : "28800"
            #"pfs": "Group5"
          }
}
)


print "3.Creating Vpn Service"


neutron.create_vpnservice(
                          body={
  "vpnservice": {
           
           #"tenant_id": "310df60f-2a10-4ee5-9554-98393092194c",
           "name": "cloud_vpn",
           "subnet_id": boot_subnet,
	   "router_id": router_id
           }
})

