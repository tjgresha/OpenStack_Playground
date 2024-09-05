import string
import random
import sys
import os
import openstack
from openstack import connection

#openstack.enable_logging(True, stream=sys.stdout)
while_loop = 1
servers_to_build=5

conn = connection.Connection(
    region_name='RegionOne',
    auth={
      'auth_url': 'http://172.232.163.233/identity',
      'username': 'admin',
      'project_id': '6269a6102c8649d48af2debfff4c543b',
      'project_name': 'admin',
      'password': os.environ.get('CLOUDPASS'),
      'user_domain_name': 'Default'
    },
    compute_api_version='2',
    identity_interface='public',
)

def list_servers(conn):
    for server in conn.compute.servers():
        print('Server Name: ' + server.hostname)


def generate_server_name():
    rnd_servername = ''.join(random.choices(string.ascii_letters,k=7))
    return (rnd_servername)

def delete_servers(conn):
    for server in conn.compute.servers():
        print('Deleting Server: ' + server.name)
        conn.compute.delete_server(server)

def create_server(conn,servername):
    image = conn.image.find_image('cirros-0.6.2-x86_64-disk')
    flavor = conn.compute.find_flavor('m1.nano')
    network = conn.network.find_network('shared')
    
    server = conn.compute.create_server(
        name=servername,
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": network.id}],
        key_name='tjgresha',
    )

    server = conn.compute.wait_for_server(server)


#let's generate servers for fun

while while_loop <= servers_to_build:
    print ("Creating Server Number: " + str(while_loop))
    create_server(conn, generate_server_name())
    while_loop += 1

delete_servers(conn)