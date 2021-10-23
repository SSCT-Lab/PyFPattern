

def main():
    module = AnsibleModule(argument_spec=dict(acpi=dict(type='bool', default='yes'), agent=dict(type='bool'), args=dict(type='str', default=None), api_host=dict(required=True), api_user=dict(required=True), api_password=dict(no_log=True), autostart=dict(type='bool', default='no'), balloon=dict(type='int', default=0), bios=dict(choices=['seabios', 'ovmf']), boot=dict(type='str', default='cnd'), bootdisk=dict(type='str'), clone=dict(type='str', default=None), cores=dict(type='int', default=1), cpu=dict(type='str', default='kvm64'), cpulimit=dict(type='int'), cpuunits=dict(type='int', default=1000), delete=dict(type='str', default=None), description=dict(type='str'), digest=dict(type='str'), force=dict(type='bool', default=None), format=dict(type='str', default='qcow2', choices=['cloop', 'cow', 'qcow', 'qcow2', 'qed', 'raw', 'vmdk']), freeze=dict(type='bool'), full=dict(type='bool', default='yes'), hostpci=dict(type='dict'), hotplug=dict(type='str'), hugepages=dict(choices=['any', '2', '1024']), ide=dict(type='dict', default=None), keyboard=dict(type='str'), kvm=dict(type='bool', default='yes'), localtime=dict(type='bool'), lock=dict(choices=['migrate', 'backup', 'snapshot', 'rollback']), machine=dict(type='str'), memory=dict(type='int', default=512), migrate_downtime=dict(type='int'), migrate_speed=dict(type='int'), name=dict(type='str'), net=dict(type='dict'), newid=dict(type='int', default=None), node=dict(), numa=dict(type='dict'), numa_enabled=dict(type='bool'), onboot=dict(type='bool', default='yes'), ostype=dict(default='l26', choices=['other', 'wxp', 'w2k', 'w2k3', 'w2k8', 'wvista', 'win7', 'win8', 'win10', 'l24', 'l26', 'solaris']), parallel=dict(type='dict'), pool=dict(type='str'), protection=dict(type='bool'), reboot=dict(type='bool'), revert=dict(type='str', default=None), sata=dict(type='dict'), scsi=dict(type='dict'), scsihw=dict(choices=['lsi', 'lsi53c810', 'virtio-scsi-pci', 'virtio-scsi-single', 'megasas', 'pvscsi']), serial=dict(type='dict'), shares=dict(type='int'), skiplock=dict(type='bool'), smbios=dict(type='str'), snapname=dict(type='str'), sockets=dict(type='int', default=1), startdate=dict(type='str'), startup=dict(), state=dict(default='present', choices=['present', 'absent', 'stopped', 'started', 'restarted', 'current']), storage=dict(type='str'), tablet=dict(type='bool', default='no'), target=dict(type='str'), tdf=dict(type='bool'), template=dict(type='bool', default='no'), timeout=dict(type='int', default=30), update=dict(type='bool', default='no'), validate_certs=dict(type='bool', default='no'), vcpus=dict(type='int', default=None), vga=dict(default='std', choices=['std', 'cirrus', 'vmware', 'qxl', 'serial0', 'serial1', 'serial2', 'serial3', 'qxl2', 'qxl3', 'qxl4']), virtio=dict(type='dict', default=None), vmid=dict(type='int', default=None), watchdog=dict()), mutually_exclusive=[('delete', 'revert'), ('delete', 'update'), ('revert', 'update'), ('clone', 'update'), ('clone', 'delete'), ('clone', 'revert')], required_one_of=[('name', 'vmid')], required_if=[('state', 'present', ['node'])])
    if (not HAS_PROXMOXER):
        module.fail_json(msg='proxmoxer required for this module')
    api_user = module.params['api_user']
    api_host = module.params['api_host']
    api_password = module.params['api_password']
    clone = module.params['clone']
    cpu = module.params['cpu']
    cores = module.params['cores']
    delete = module.params['delete']
    memory = module.params['memory']
    name = module.params['name']
    newid = module.params['newid']
    node = module.params['node']
    revert = module.params['revert']
    sockets = module.params['sockets']
    state = module.params['state']
    timeout = module.params['timeout']
    update = bool(module.params['update'])
    vmid = module.params['vmid']
    validate_certs = module.params['validate_certs']
    if (not api_password):
        try:
            api_password = os.environ['PROXMOX_PASSWORD']
        except KeyError as e:
            module.fail_json(msg='You should set api_password param or use PROXMOX_PASSWORD environment variable')
    try:
        proxmox = ProxmoxAPI(api_host, user=api_user, password=api_password, verify_ssl=validate_certs)
        global VZ_TYPE
        global PVE_MAJOR_VERSION
        PVE_MAJOR_VERSION = (3 if (float(proxmox.version.get()['version']) < 4.0) else 4)
    except Exception as e:
        module.fail_json(msg=('authorization on proxmox cluster failed with exception: %s' % e))
    if (not vmid):
        if ((state == 'present') and ((not update) and (not clone)) and ((not delete) and (not revert))):
            try:
                vmid = get_nextvmid(module, proxmox)
            except Exception as e:
                module.fail_json(msg="Can't get the next vmid for VM {0} automatically. Ensure your cluster state is good".format(name))
        else:
            try:
                if (not clone):
                    vmid = get_vmid(proxmox, name)[0]
                else:
                    vmid = get_vmid(proxmox, clone)[0]
            except Exception as e:
                if (not clone):
                    module.fail_json(msg='VM {0} does not exist in cluster.'.format(name))
                else:
                    module.fail_json(msg='VM {0} does not exist in cluster.'.format(clone))
    if (clone is not None):
        if get_vmid(proxmox, name):
            module.exit_json(changed=False, msg=('VM with name <%s> already exists' % name))
        if (vmid is not None):
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s does not exist in cluster' % vmid))
        if (not newid):
            try:
                newid = get_nextvmid(module, proxmox)
            except Exception as e:
                module.fail_json(msg="Can't get the next vmid for VM {0} automatically. Ensure your cluster state is good".format(name))
        else:
            vm = get_vm(proxmox, newid)
            if vm:
                module.exit_json(changed=False, msg=('vmid %s with VM name %s already exists' % (newid, name)))
    if (delete is not None):
        try:
            settings(module, proxmox, vmid, node, name, timeout, delete=delete)
            module.exit_json(changed=True, msg='Settings has deleted on VM {0} with vmid {1}'.format(name, vmid))
        except Exception as e:
            module.fail_json(msg=('Unable to delete settings on VM {0} with vmid {1}: '.format(name, vmid) + str(e)))
    elif (revert is not None):
        try:
            settings(module, proxmox, vmid, node, name, timeout, revert=revert)
            module.exit_json(changed=True, msg='Settings has reverted on VM {0} with vmid {1}'.format(name, vmid))
        except Exception as e:
            module.fail_json(msg=('Unable to revert settings on VM {0} with vmid {1}: Maybe is not a pending task...   '.format(name, vmid) + str(e)))
    if (state == 'present'):
        try:
            if (get_vm(proxmox, vmid) and (not (update or clone))):
                module.exit_json(changed=False, msg=('VM with vmid <%s> already exists' % vmid))
            elif (get_vmid(proxmox, name) and (not (update or clone))):
                module.exit_json(changed=False, msg=('VM with name <%s> already exists' % name))
            elif (not (node, name)):
                module.fail_json(msg='node, name is mandatory for creating/updating vm')
            elif (not node_check(proxmox, node)):
                module.fail_json(msg=("node '%s' does not exist in cluster" % node))
            create_vm(module, proxmox, vmid, newid, node, name, memory, cpu, cores, sockets, timeout, update, acpi=module.params['acpi'], agent=module.params['agent'], autostart=module.params['autostart'], balloon=module.params['balloon'], bios=module.params['bios'], boot=module.params['boot'], bootdisk=module.params['bootdisk'], cpulimit=module.params['cpulimit'], cpuunits=module.params['cpuunits'], description=module.params['description'], digest=module.params['digest'], force=module.params['force'], freeze=module.params['freeze'], hostpci=module.params['hostpci'], hotplug=module.params['hotplug'], hugepages=module.params['hugepages'], ide=module.params['ide'], keyboard=module.params['keyboard'], kvm=module.params['kvm'], localtime=module.params['localtime'], lock=module.params['lock'], machine=module.params['machine'], migrate_downtime=module.params['migrate_downtime'], migrate_speed=module.params['migrate_speed'], net=module.params['net'], numa=module.params['numa'], numa_enabled=module.params['numa_enabled'], onboot=module.params['onboot'], ostype=module.params['ostype'], parallel=module.params['parallel'], pool=module.params['pool'], protection=module.params['protection'], reboot=module.params['reboot'], sata=module.params['sata'], scsi=module.params['scsi'], scsihw=module.params['scsihw'], serial=module.params['serial'], shares=module.params['shares'], skiplock=module.params['skiplock'], smbios1=module.params['smbios'], snapname=module.params['snapname'], startdate=module.params['startdate'], startup=module.params['startup'], tablet=module.params['tablet'], target=module.params['target'], tdf=module.params['tdf'], template=module.params['template'], vcpus=module.params['vcpus'], vga=module.params['vga'], virtio=module.params['virtio'], watchdog=module.params['watchdog'])
            if (not clone):
                get_vminfo(module, proxmox, node, vmid, ide=module.params['ide'], net=module.params['net'], sata=module.params['sata'], scsi=module.params['scsi'], virtio=module.params['virtio'])
            if update:
                module.exit_json(changed=True, msg=('VM %s with vmid %s updated' % (name, vmid)))
            elif (clone is not None):
                module.exit_json(changed=True, msg=('VM %s with newid %s cloned from vm with vmid %s' % (name, newid, vmid)))
            else:
                module.exit_json(changed=True, msg=('VM %s with vmid %s deployed' % (name, vmid)), **results)
        except Exception as e:
            if update:
                module.fail_json(msg=('Unable to update vm {0} with vmid {1}='.format(name, vmid) + str(e)))
            elif (clone is not None):
                module.fail_json(msg=('Unable to clone vm {0} from vmid {1}='.format(name, vmid) + str(e)))
            else:
                module.fail_json(msg=('creation of %s VM %s with vmid %s failed with exception=%s' % (VZ_TYPE, name, vmid, e)))
    elif (state == 'started'):
        try:
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid <%s> does not exist in cluster' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'running'):
                module.exit_json(changed=False, msg=('VM %s is already running' % vmid))
            if start_vm(module, proxmox, vm, vmid, timeout):
                module.exit_json(changed=True, msg=('VM %s started' % vmid))
        except Exception as e:
            module.fail_json(msg=('starting of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'stopped'):
        try:
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s does not exist in cluster' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'stopped'):
                module.exit_json(changed=False, msg=('VM %s is already stopped' % vmid))
            if stop_vm(module, proxmox, vm, vmid, timeout, force=module.params['force']):
                module.exit_json(changed=True, msg=('VM %s is shutting down' % vmid))
        except Exception as e:
            module.fail_json(msg=('stopping of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'restarted'):
        try:
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s does not exist in cluster' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'stopped'):
                module.exit_json(changed=False, msg=('VM %s is not running' % vmid))
            if (stop_vm(module, proxmox, vm, vmid, timeout, force=module.params['force']) and start_vm(module, proxmox, vm, vmid, timeout)):
                module.exit_json(changed=True, msg=('VM %s is restarted' % vmid))
        except Exception as e:
            module.fail_json(msg=('restarting of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'absent'):
        try:
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.exit_json(changed=False, msg=('VM %s does not exist' % vmid))
            if (getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status'] == 'running'):
                module.exit_json(changed=False, msg=('VM %s is running. Stop it before deletion.' % vmid))
            taskid = getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE).delete(vmid)
            while timeout:
                if ((proxmox.nodes(vm[0]['node']).tasks(taskid).status.get()['status'] == 'stopped') and (proxmox.nodes(vm[0]['node']).tasks(taskid).status.get()['exitstatus'] == 'OK')):
                    module.exit_json(changed=True, msg=('VM %s removed' % vmid))
                timeout -= 1
                if (timeout == 0):
                    module.fail_json(msg=('Reached timeout while waiting for removing VM. Last line in task before timeout: %s' % proxmox.nodes(vm[0]['node']).tasks(taskid).log.get()[:1]))
                time.sleep(1)
        except Exception as e:
            module.fail_json(msg=('deletion of VM %s failed with exception: %s' % (vmid, e)))
    elif (state == 'current'):
        status = {
            
        }
        try:
            vm = get_vm(proxmox, vmid)
            if (not vm):
                module.fail_json(msg=('VM with vmid = %s does not exist in cluster' % vmid))
            current = getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).status.current.get()['status']
            status['status'] = current
            if status:
                module.exit_json(changed=False, msg=('VM %s with vmid = %s is %s' % (name, vmid, current)), **status)
        except Exception as e:
            module.fail_json(msg=('Unable to get vm {0} with vmid = {1} status: '.format(name, vmid) + str(e)))
