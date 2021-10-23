def create_single_device(module, packet_conn, hostname):
    for param in ('hostnames', 'operating_system', 'plan'):
        if (not module.params.get(param)):
            raise Exception(('%s parameter is required for new device.' % param))
    project_id = module.params.get('project_id')
    plan = module.params.get('plan')
    user_data = module.params.get('user_data')
    facility = module.params.get('facility')
    operating_system = module.params.get('operating_system')
    locked = module.params.get('locked')
    ipxe_script_url = module.params.get('ipxe_script_url')
    always_pxe = module.params.get('always_pxe')
    device = packet_conn.create_device(project_id=project_id, hostname=hostname, plan=plan, facility=facility, operating_system=operating_system, userdata=user_data, locked=locked)
    return device