def main():
    module = AnsibleModule(argument_spec=dict(state=dict(type='str', default='present', choices=['absent', 'active', 'deleted', 'present', 'restarted', 'started', 'stopped']), api_key=dict(type='str', no_log=True), name=dict(type='str'), alert_bwin_enabled=dict(type='bool'), alert_bwin_threshold=dict(type='int'), alert_bwout_enabled=dict(type='bool'), alert_bwout_threshold=dict(type='int'), alert_bwquota_enabled=dict(type='bool'), alert_bwquota_threshold=dict(type='int'), alert_cpu_enabled=dict(type='bool'), alert_cpu_threshold=dict(type='int'), alert_diskio_enabled=dict(type='bool'), alert_diskio_threshold=dict(type='int'), backupsenabled=dict(type='int'), backupweeklyday=dict(type='int'), backupwindow=dict(type='int'), displaygroup=dict(type='str', default=''), plan=dict(type='int'), additional_disks=dict(type='list'), distribution=dict(type='int'), datacenter=dict(type='int'), kernel_id=dict(type='int'), linode_id=dict(type='int', aliases=['lid']), payment_term=dict(type='int', default=1, choices=[1, 12, 24]), password=dict(type='str', no_log=True), private_ip=dict(type='bool'), ssh_pub_key=dict(type='str'), swap=dict(type='int', default=512), wait=dict(type='bool', default=True), wait_timeout=dict(default=300), watchdog=dict(type='bool', default=True)))
    if (not HAS_LINODE):
        module.fail_json(msg='linode-python required for this module')
    state = module.params.get('state')
    api_key = module.params.get('api_key')
    name = module.params.get('name')
    alert_bwin_enabled = module.params.get('alert_bwin_enabled')
    alert_bwin_threshold = module.params.get('alert_bwin_threshold')
    alert_bwout_enabled = module.params.get('alert_bwout_enabled')
    alert_bwout_threshold = module.params.get('alert_bwout_threshold')
    alert_bwquota_enabled = module.params.get('alert_bwquota_enabled')
    alert_bwquota_threshold = module.params.get('alert_bwquota_threshold')
    alert_cpu_enabled = module.params.get('alert_cpu_enabled')
    alert_cpu_threshold = module.params.get('alert_cpu_threshold')
    alert_diskio_enabled = module.params.get('alert_diskio_enabled')
    alert_diskio_threshold = module.params.get('alert_diskio_threshold')
    backupsenabled = module.params.get('backupsenabled')
    backupweeklyday = module.params.get('backupweeklyday')
    backupwindow = module.params.get('backupwindow')
    displaygroup = module.params.get('displaygroup')
    plan = module.params.get('plan')
    additional_disks = module.params.get('additional_disks')
    distribution = module.params.get('distribution')
    datacenter = module.params.get('datacenter')
    kernel_id = module.params.get('kernel_id')
    linode_id = module.params.get('linode_id')
    payment_term = module.params.get('payment_term')
    password = module.params.get('password')
    private_ip = module.params.get('private_ip')
    ssh_pub_key = module.params.get('ssh_pub_key')
    swap = module.params.get('swap')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    watchdog = int(module.params.get('watchdog'))
    kwargs = dict()
    check_items = dict(alert_bwin_enabled=alert_bwin_enabled, alert_bwin_threshold=alert_bwin_threshold, alert_bwout_enabled=alert_bwout_enabled, alert_bwout_threshold=alert_bwout_threshold, alert_bwquota_enabled=alert_bwquota_enabled, alert_bwquota_threshold=alert_bwquota_threshold, alert_cpu_enabled=alert_cpu_enabled, alert_cpu_threshold=alert_cpu_threshold, alert_diskio_enabled=alert_diskio_enabled, alert_diskio_threshold=alert_diskio_threshold, backupweeklyday=backupweeklyday, backupwindow=backupwindow)
    for (key, value) in check_items.items():
        if (value is not None):
            kwargs[key] = value
    if (not api_key):
        try:
            api_key = os.environ['LINODE_API_KEY']
        except KeyError as e:
            module.fail_json(msg=('Unable to load %s' % e.message))
    try:
        api = linode_api.Api(api_key)
        api.test_echo()
    except Exception as e:
        module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
    linodeServers(module, api, state, name, displaygroup, plan, additional_disks, distribution, datacenter, kernel_id, linode_id, payment_term, password, private_ip, ssh_pub_key, swap, wait, wait_timeout, watchdog, **kwargs)