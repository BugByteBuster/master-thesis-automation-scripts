import sys
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as keystoneclient
from glanceclient.v2 import Client
from neutronclient.v2_0 import client

def main():
    url = "http://" + sys.argv[1] + "/identity/v3"
    auth = v3.Password(auth_url=url, username="admin",
                       password="password", project_name="demopro1",
                       user_domain_id="default", project_domain_id="default")
    sess = session.Session(auth=auth)
    
    if sys.argv[1] == '192.168.2.7':
        cidr = "192.168.2.0/24"
    elif sys.argv[1] == '192.168.2.8':
        cidr = "192.168.3.0/24"
    elif sys.argv[1] == '192.168.2.9':
        cidr = "192.168.4.0/24"
    
    glance = create_glance_client(sess)
    boot_image = get_boot_image(glance)
    
    neutron = create_neutron_client(sess)
    boot_subnet = create_subnet(neutron, cidr)
    
    nova = create_nova_client(sess)
    boot_flav = get_boot_flavor(nova)
    instance_boot = boot_instance(nova, boot_image, boot_flav, boot_subnet)
    
    router_id = create_router(neutron, boot_subnet)
    create_vpn(neutron, boot_subnet, router_id)

def create_glance_client(session):
    return Client(session=session)

def get_boot_image(glance):
    available_images = []
    for image in glance.images.list():
        available_images.append(image.id)
    return available_images[0]

def create_neutron_client(session):
    return client.Client(session=session)

def create_subnet(neutron, cidr):
    subnets = neutron.list_subnets()
    print "creating network....."
    networks = neutron.list_networks(name='public')
    external_netid = networks['networks'][0]['id']
    net = neutron.create_network(
        body={
            "network": {
                "name": "net1",
                "admin_state_up": True
            }
        }
    )
    
    boot_net = net['network']['id']
    print "creating subnet......"
    subnet = neutron.create_subnet(
        body={
            "subnet": {
                "name": "subnet1",
                "network_id": boot_net,
                "ip_version": 4,
                "cidr": cidr
            }
        }
    )
    
    return subnet['subnet']['id']

def create_nova_client(session):
    return client.Client('2.1', session=session)

def get_boot_flavor(nova):
    return nova.flavors.find(name='m1.nano')

def boot_instance(nova, boot_image, boot_flav, boot_subnet):
    print "booting instance...."
    return nova.servers.create(
        name="instance1",
        image=boot_image,
        flavor=boot_flav,
        network=boot_subnet
    )

def create_router(neutron, boot_subnet):
    print "Creating the router and adding the interfaces......"
    router = neutron.create_router(
        body={
            "router": {
                "name": "router1",
                "external_gateway_info": {
                    "network_id": external_netid,
                    "enable_snat": True
                },
                "admin_state_up": True
            }
        }
    )

    router_id = router['router']['id']
    neutron.add_interface_router(
        router_id,
        body={
            "subnet_id": boot_subnet
        }
    )
    return router_id

def create_vpn(neutron, boot_subnet, router_id):
    print "Setting UP VPN"
    print "1.Creating IKE Policy..."
    neutron.create_ikepolicy(
        body={
            "ikepolicy": {
                "name": "ikepolicy_1",
                "auth_algorithm": "sha1",
                "encryption_algorithm": "aes-256",
                "phase1_negotiation_mode": "main"
            }
        }
    )

    print "2.Creating IPSEC Policy ......"
    neutron.create_ipsecpolicy(
        body={
            "ipsecpolicy": {
                "name": "ipsecpolicy_1",
                "transform_protocol": "esp",
                "auth_algorithm": "sha1",
                "encryption_algorithm": "aes-256",
                "encapsulation_mode": "tunnel"
            }
        }
    )

    print "3.Creating Vpn Service"
    neutron.create_vpnservice(
        body={
            "vpnservice": {
                "name": "cloud_vpn",
                "subnet_id": boot_subnet,
                "router_id": router_id
            }
        }
    )

if __name__ == "__main__":
    main()
