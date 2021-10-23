def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(aliases=['host'], required=True), bond=dict(default=None, type='dict'), interface=dict(default=None), networks=dict(default=None, type='list'), labels=dict(default=None, type='list'), check=dict(default=None, type='bool'), save=dict(default=None, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        host_networks_module = HostNetworksModule(connection=connection, module=module, service=hosts_service)
        host = host_networks_module.search_entity()
        if (host is None):
            raise Exception(("Host '%s' was not found." % module.params['name']))
        bond = module.params['bond']
        interface = module.params['interface']
        networks = module.params['networks']
        labels = module.params['labels']
        nic_name = (bond.get('name') if bond else module.params['interface'])
        host_service = hosts_service.host_service(host.id)
        nics_service = host_service.nics_service()
        nic = search_by_name(nics_service, nic_name)
        network_names = [network['name'] for network in (networks or [])]
        state = module.params['state']
        if ((state == 'present') and ((nic is None) or host_networks_module.has_update(nics_service.service(nic.id)))):
            attachments_service = host_service.network_attachments_service()
            for a in attachments_service.list():
                current_network_name = get_link_name(connection, a.network)
                if (current_network_name in network_names):
                    for n in networks:
                        if (n['name'] == current_network_name):
                            n['id'] = a.id
            removed_bonds = []
            if (nic is not None):
                for host_nic in nics_service.list():
                    if (host_nic.bonding and (nic.id in [slave.id for slave in host_nic.bonding.slaves])):
                        removed_bonds.append(otypes.HostNic(id=host_nic.id))
            host_networks_module.action(entity=host, action='setup_networks', post_action=host_networks_module._action_save_configuration, check_connectivity=module.params['check'], removed_bonds=(removed_bonds if removed_bonds else None), modified_bonds=([otypes.HostNic(name=bond.get('name'), bonding=otypes.Bonding(options=get_bond_options(bond.get('mode'), bond.get('options')), slaves=[otypes.HostNic(name=i) for i in bond.get('interfaces', [])]))] if bond else None), modified_labels=([otypes.NetworkLabel(id=str(name), host_nic=otypes.HostNic(name=(bond.get('name') if bond else interface))) for name in labels] if labels else None), modified_network_attachments=([otypes.NetworkAttachment(id=network.get('id'), network=(otypes.Network(name=network['name']) if network['name'] else None), host_nic=otypes.HostNic(name=(bond.get('name') if bond else interface)), ip_address_assignments=[otypes.IpAddressAssignment(assignment_method=otypes.BootProtocol(network.get('boot_protocol', 'none')), ip=otypes.Ip(address=network.get('address'), gateway=network.get('gateway'), netmask=network.get('netmask'), version=(otypes.IpVersion(network.get('version')) if network.get('version') else None)))]) for network in networks] if networks else None))
        elif ((state == 'absent') and nic):
            attachments = []
            nic_service = nics_service.nic_service(nic.id)
            attached_labels = set([str(lbl.id) for lbl in nic_service.network_labels_service().list()])
            if networks:
                attachments_service = nic_service.network_attachments_service()
                attachments = attachments_service.list()
                attachments = [attachment for attachment in attachments if (get_link_name(connection, attachment.network) in network_names)]
            unmanaged_networks_service = host_service.unmanaged_networks_service()
            unmanaged_networks = [(u.id, u.name) for u in unmanaged_networks_service.list()]
            for (net_id, net_name) in unmanaged_networks:
                if (net_name in network_names):
                    if (not module.check_mode):
                        unmanaged_networks_service.unmanaged_network_service(net_id).remove()
                    host_networks_module.changed = True
            if ((labels and set(labels).intersection(attached_labels)) or bond or attachments):
                host_networks_module.action(entity=host, action='setup_networks', post_action=host_networks_module._action_save_configuration, check_connectivity=module.params['check'], removed_bonds=([otypes.HostNic(name=bond.get('name'))] if bond else None), removed_labels=([otypes.NetworkLabel(id=str(name)) for name in labels] if labels else None), removed_network_attachments=(attachments if attachments else None))
        nic = search_by_name(nics_service, nic_name)
        module.exit_json(**{
            'changed': host_networks_module.changed,
            'id': (nic.id if nic else None),
            'host_nic': get_dict_of_struct(nic),
        })
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))