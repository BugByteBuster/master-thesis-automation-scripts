import sys
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as keystoneclient
from novaclient import client
from glanceclient.v2 import Client
from neutronclient.v2_0 import client

cloud_ips = []

def main():
    for i in range(1, len(sys.argv)):
        if sys.argv[i] not in cloud_ips:
            cloud_ips.append(sys.argv[i])
    if len(cloud_ips) > 1:
        auth_url = "http://" + cloud_ips[i] + "/identity/v3"
        connect(auth_url)
        image_select()

    if sys.argv[1] == '192.168.2.7':
        cidr = "192.168.2.0/24"
    elif sys.argv[1] == '192.168.2.8':
        cidr = "192.168.3.0/24"
    elif sys.argv[1] == '192.168.2.9':
        cidr = "192.168.4.0/24"

    create_network()
    boot_instance()
    router_create()
    vpn_setup()

def connect(auth_url):
    auth = v3.Password(
        auth_url=auth_url,
        username="admin",
        password="password",
        project_name="demopro1",
        user_domain_id="default",
        project_domain_id="default"
    )
    global sess
    sess = session.Session(auth=auth)

def image_select():
    glance = Client(session=sess)
    available_images = []
    for image in glance.images.list():
        available_images.append(image.id)
    boot_image = available_images[0]

def create_network():
    neutron = client.Client(session=sess)
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

    boot_subnet = subnet['subnet']['id']
    peer_subnet = subnet['subnet']['cidr']

def boot_instance():
    nova = client.Client('2.1', session=sess)
    boot_flav = nova.flavors.find(name='m1.nano')
    print "booting instance...."
    instance_boot = nova.servers.create(
        name="instance1",
        image=boot_image,
        flavor=boot_flav,
        network=boot_subnet
    )

def router_create():
    print "Creating the router and adding the interfaces......"
    neutron = client.Client(session=sess)
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
    neutron.add_interface_router(router_id, body={"subnet_id": boot_subnet})
    peer_cidr = neutron._get_external_gw_ips['router_id']
    router_gateway = router['router']['external_gateway_info']
    print peer_cidr

def vpn_setup():
    print "Setting UP VPN"

    print "1.Creating IKE Policy..."
    neutron = client.Client(session=sess)
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
