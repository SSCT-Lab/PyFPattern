def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), data_center=dict(required=True), id=dict(default=None), name=dict(required=True), description=dict(default=None), comment=dict(default=None), external_provider=dict(default=None), vlan_tag=dict(default=None, type='int'), vm_network=dict(default=None, type='bool'), mtu=dict(default=None, type='int'), clusters=dict(default=None, type='list'), label=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    check_params(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        clusters_service = connection.system_service().clusters_service()
        networks_service = connection.system_service().networks_service()
        networks_module = NetworksModule(connection=connection, module=module, service=networks_service)
        state = module.params['state']
        search_params = {
            'name': module.params['name'],
            'datacenter': module.params['data_center'],
        }
        if (state == 'present'):
            imported = False
            if (module.params.get('external_provider') and (module.params.get('name') not in [net.name for net in networks_service.list()])):
                ons_service = connection.system_service().openstack_network_providers_service()
                on_service = ons_service.provider_service(get_id_by_name(ons_service, module.params.get('external_provider')))
                on_networks_service = on_service.networks_service()
                if (module.params.get('name') in [net.name for net in on_networks_service.list()]):
                    network_service = on_networks_service.network_service(get_id_by_name(on_networks_service, module.params.get('name')))
                    network_service.import_(data_center=otypes.DataCenter(name=module.params.get('data_center')))
                    imported = True
            ret = networks_module.create(search_params=search_params)
            ret['changed'] = (ret['changed'] or imported)
            if (module.params.get('clusters') is not None):
                for param_cluster in module.params.get('clusters'):
                    cluster = search_by_name(clusters_service, param_cluster.get('name'))
                    if (cluster is None):
                        raise Exception(("Cluster '%s' was not found." % param_cluster.get('name')))
                    cluster_networks_service = clusters_service.service(cluster.id).networks_service()
                    cluster_networks_module = ClusterNetworksModule(network_id=ret['id'], cluster_network=param_cluster, connection=connection, module=module, service=cluster_networks_service)
                    if param_cluster.get('assigned', True):
                        ret = cluster_networks_module.create()
                    else:
                        ret = cluster_networks_module.remove()
        elif (state == 'absent'):
            ret = networks_module.remove(search_params=search_params)
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))