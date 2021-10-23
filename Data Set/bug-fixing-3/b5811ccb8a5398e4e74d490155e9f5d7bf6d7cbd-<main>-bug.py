def main():
    module = AnsibleModule(argument_spec=dict(api_host=dict(required=True), api_user=dict(required=True), api_password=dict(no_log=True), vmid=dict(required=False), validate_certs=dict(type='bool', default='no'), node=dict(), pool=dict(), password=dict(no_log=True), hostname=dict(), ostemplate=dict(), disk=dict(type='str', default='3'), cpus=dict(type='int', default=1), memory=dict(type='int', default=512), swap=dict(type='int', default=0), netif=dict(type='dict'), mounts=dict(type='dict'), ip_address=dict(), onboot=dict(type='bool', default='no'), storage=dict(default='local'), cpuunits=dict(type='int', default=1000), nameserver=dict(), searchdomain=dict(), timeout=dict(type='int', default=30), force=dict(type='bool', default='no'), state=dict(default='present', choices=['present', 'absent', 'stopped', 'started', 'restarted'])))
    if (not HAS_PROXMOXER):
        module.fail_json(msg='proxmoxer required for this module')
    state = module.params['state']
    api_user = module.params['api_user']
    api_host = module.params['api_host']
    api_password = module.params['api_password']
    vmid = module.params['vmid']
    validate_certs = module.params['validate_certs']
    node = module.params['node']
    disk = module.params['disk']
    cpus = module.params['cpus']
    memory = module.params['memory']
    swap = module.params['swap']
    storage = module.params['storage']
    hostname = module.params['hostname']
    if (module.params['ostemplate'] is not None):
        template_store = module.params['ostemplate'].split(':')[0]
    timeout = module.params['timeout']
    if (not api_password):
        try:
            api_password = os.environ['PROXMOX_PASSWORD']
        except KeyError as e:
            module.fail_json(msg='You should set api_password param or use PROXMOX_PASSWORD environment variable')
    try:
        proxmox = ProxmoxAPI(api_host, user=api_user, password=api_password, verify_ssl=validate_certs)
        global VZ_TYPE
        VZ_TYPE = ('openvz' if (float(proxmox.version.get()['version']) < 4.0) else 'lxc')
    except Exception as e:
        module.fail_json(msg=('authorization on proxmox cluster failed with exception: %s' % e))
    if ((not vmid) and (state == 'present')):
        vmid = get_nextvmid(proxmox)
    elif ((not vmid) and hostname):
        vmid = get_vmid(proxmox, hostname)[0]
    elif (not vmid):
        module.exit_json(changed=False, msg=('Vmid could not be fetched for the following action: %s' % state))
    if (state == 'present'):
        try:
            if (get_instance(proxmox, vmid) and (not module.params['force'])):
                module.exit_json(changed=False, msg=('VM with vmid = %s is already exists' % vmid))
            if ((not module.params['vmid']) and get_vmid(proxmox, hostname) and (not module.params['force'])):
                module.exit_json(changed=False, msg=('VM with hostname %s already exists and has ID number %s' % (hostname, get_vmid(proxmox, hostname)[0])))
            elif (not (node, (module.params['hostname'] and module.params['password'] and module.params['ostemplate']))):
                module.fail_json(msg='node, hostname, password and ostemplate are mandatory for creating vm')
            elif (not node_check(proxmox, node)):
                module.fail_json(msg=("node '%s' not exists in cluster" % node))
            elif (not content_check(proxmox, node, module.params['ostemplate'], template_store)):
                module.fail_json(msg=("ostemplate '%s' not exists on node %s and storage %s" % (module.params['ostemplate'], node, template_store)))
            create_instance(module, proxmox, vmid, node, disk, storage, cpus, memory, swap, timeout, pool=module.params['pool'], password=module.params['password'], hostname=module.params['hostname'], ostemplate=module.params['ostemplate'], netif=module.params['netif'], mounts=module.params['mounts'], ip_address=module.params['ip_address'], onboot=int(module.params['onboot']), cpuunits=module.params['cpuunits'], nameserver=module.params['nameserver'], searchdomain=module.params['searchdomain'], force=int(module.params['force']))
            module.exit_json(changed=True, msg=('deployed VM %s from template %s' % (vmid, module.params['ostemplate'])))
        except Exception as e:
            module.fail_json(msg=('creation of %s VM %s failed with exception: %s' % (VZ_TYPE, vmid, e)))
    elif (state == 'started'):
        try:
            vm = get_instance(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s not exists in cluster' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'running'):
                module.exit_json(changed=False, msg=('VM %s is already running' % vmid))
            if start_instance(module, proxmox, vm, vmid, timeout):
                module.exit_json(changed=True, msg=('VM %s started' % vmid))
        except Exception as e:
            module.fail_json(msg=('starting of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'stopped'):
        try:
            vm = get_instance(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s not exists in cluster' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'mounted'):
                if module.params['force']:
                    if umount_instance(module, proxmox, vm, vmid, timeout):
                        module.exit_json(changed=True, msg=('VM %s is shutting down' % vmid))
                else:
                    module.exit_json(changed=False, msg=('VM %s is already shutdown, but mounted. You can use force option to umount it.' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'stopped'):
                module.exit_json(changed=False, msg=('VM %s is already shutdown' % vmid))
            if stop_instance(module, proxmox, vm, vmid, timeout, force=module.params['force']):
                module.exit_json(changed=True, msg=('VM %s is shutting down' % vmid))
        except Exception as e:
            module.fail_json(msg=('stopping of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'restarted'):
        try:
            vm = get_instance(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s not exists in cluster' % vmid))
            if ((getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'stopped') or (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'mounted')):
                module.exit_json(changed=False, msg=('VM %s is not running' % vmid))
            if (stop_instance(module, proxmox, vm, vmid, timeout, force=module.params['force']) and start_instance(module, proxmox, vm, vmid, timeout)):
                module.exit_json(changed=True, msg=('VM %s is restarted' % vmid))
        except Exception as e:
            module.fail_json(msg=('restarting of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'absent'):
        try:
            vm = get_instance(proxmox, vmid)
            if (not vm):
                module.exit_json(changed=False, msg=('VM %s does not exist' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'running'):
                module.exit_json(changed=False, msg=('VM %s is running. Stop it before deletion.' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'mounted'):
                module.exit_json(changed=False, msg=('VM %s is mounted. Stop it with force option before deletion.' % vmid))
            taskid = getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE).delete(vmid)
            while timeout:
                if ((proxmox.nodes(vm[0]['node']).tasks(taskid).status.get()['status'] == 'stopped') and (proxmox.nodes(vm[0]['node']).tasks(taskid).status.get()['exitstatus'] == 'OK')):
                    module.exit_json(changed=True, msg=('VM %s removed' % vmid))
                timeout = (timeout - 1)
                if (timeout == 0):
                    module.fail_json(msg=('Reached timeout while waiting for removing VM. Last line in task before timeout: %s' % proxmox_node.tasks(taskid).log.get()[:1]))
                time.sleep(1)
        except Exception as e:
            module.fail_json(msg=('deletion of VM %s failed with exception: %s' % (vmid, e)))