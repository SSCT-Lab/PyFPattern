

def main():
    argument_spec = openstack_full_argument_spec(server=dict(required=True), state=dict(default='present', choices=['absent', 'present']), network=dict(required=False, default=None), floating_ip_address=dict(required=False, default=None), reuse=dict(required=False, type='bool', default=False), fixed_address=dict(required=False, default=None), nat_destination=dict(required=False, default=None, aliases=['fixed_network', 'internal_network']), wait=dict(required=False, type='bool', default=False), timeout=dict(required=False, type='int', default=60), purge=dict(required=False, type='bool', default=False))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    server_name_or_id = module.params['server']
    state = module.params['state']
    network = module.params['network']
    floating_ip_address = module.params['floating_ip_address']
    reuse = module.params['reuse']
    fixed_address = module.params['fixed_address']
    nat_destination = module.params['nat_destination']
    wait = module.params['wait']
    timeout = module.params['timeout']
    purge = module.params['purge']
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        server = cloud.get_server(server_name_or_id)
        if (server is None):
            module.fail_json(msg='server {0} not found'.format(server_name_or_id))
        if (state == 'present'):
            public_ip = cloud.get_server_public_ip(server)
            f_ip = (_get_floating_ip(cloud, public_ip) if public_ip else public_ip)
            if f_ip:
                if network:
                    network_id = cloud.get_network(name_or_id=network)['id']
                else:
                    network_id = None
                if nat_destination:
                    nat_floating_addrs = [addr for addr in server.addresses.get(cloud.get_network(nat_destination)['name'], []) if ((addr.addr == public_ip) and (addr['OS-EXT-IPS:type'] == 'floating'))]
                    if (len(nat_floating_addrs) == 0):
                        module.fail_json(msg="server {server} already has a floating-ip on a different nat-destination than '{nat_destination}'".format(server=server_name_or_id, nat_destination=nat_destination))
                if all([fixed_address, (f_ip.fixed_ip_address == fixed_address), network, (f_ip.network != network_id)]):
                    module.fail_json(msg="server {server} already has a floating-ip on requested interface but it doesn't match requested network {network}: {fip}".format(server=server_name_or_id, network=network, fip=remove_values(f_ip, module.no_log_values)))
                if ((not network) or (f_ip.network == network_id)):
                    module.exit_json(changed=False, floating_ip=f_ip)
            server = cloud.add_ips_to_server(server=server, ips=floating_ip_address, ip_pool=network, reuse=reuse, fixed_address=fixed_address, wait=wait, timeout=timeout, nat_destination=nat_destination)
            fip_address = cloud.get_server_public_ip(server)
            f_ip = _get_floating_ip(cloud, fip_address)
            module.exit_json(changed=True, floating_ip=f_ip)
        elif (state == 'absent'):
            if (floating_ip_address is None):
                if (not server_name_or_id):
                    module.fail_json(msg='either server or floating_ip_address are required')
                server = cloud.get_server(server_name_or_id)
                floating_ip_address = cloud.get_server_public_ip(server)
            f_ip = _get_floating_ip(cloud, floating_ip_address)
            if (not f_ip):
                module.exit_json(changed=False)
            changed = False
            if f_ip['fixed_ip_address']:
                cloud.detach_ip_from_server(server_id=server['id'], floating_ip_id=f_ip['id'])
                f_ip = cloud.get_floating_ip(id=f_ip['id'])
                changed = True
            if purge:
                cloud.delete_floating_ip(f_ip['id'])
                module.exit_json(changed=True)
            module.exit_json(changed=changed, floating_ip=f_ip)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)
