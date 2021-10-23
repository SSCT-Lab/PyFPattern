

def main():
    vm = None
    proto_vm_hardware = {
        'memory_mb': int,
        'num_cpus': int,
        'scsi': string_types,
        'osid': string_types,
    }
    proto_vm_disk = {
        'disk1': {
            'datastore': string_types,
            'size_gb': int,
            'type': string_types,
        },
    }
    proto_vm_nic = {
        'nic1': {
            'type': string_types,
            'network': string_types,
            'network_type': string_types,
        },
    }
    proto_esxi = {
        'datacenter': string_types,
        'hostname': string_types,
    }
    module = AnsibleModule(argument_spec=dict(vcenter_hostname=dict(type='str', default=os.environ.get('VMWARE_HOST')), username=dict(type='str', default=os.environ.get('VMWARE_USER')), password=dict(type='str', no_log=True, default=os.environ.get('VMWARE_PASSWORD')), state=dict(required=False, choices=['powered_on', 'powered_off', 'present', 'absent', 'restarted', 'reconfigured'], default='present'), vmware_guest_facts=dict(required=False, type='bool'), from_template=dict(required=False, type='bool'), template_src=dict(required=False, type='str'), snapshot_to_clone=dict(required=False, default=None, type='str'), guest=dict(required=True, type='str'), vm_disk=dict(required=False, type='dict', default={
        
    }), vm_nic=dict(required=False, type='dict', default={
        
    }), vm_hardware=dict(required=False, type='dict', default={
        
    }), vm_extra_config=dict(required=False, type='dict', default={
        
    }), vm_hw_version=dict(required=False, default=None, type='str'), resource_pool=dict(required=False, default=None, type='str'), cluster=dict(required=False, default=None, type='str'), force=dict(required=False, type='bool', default=False), esxi=dict(required=False, type='dict', default={
        
    }), validate_certs=dict(required=False, type='bool', default=True), power_on_after_clone=dict(required=False, type='bool', default=True)), supports_check_mode=False, mutually_exclusive=[['state', 'vmware_guest_facts'], ['state', 'from_template']], required_together=[['state', 'force'], ['state', 'vm_disk', 'vm_nic', 'vm_hardware', 'esxi'], ['from_template', 'template_src']])
    module.deprecate("The 'vsphere_guest' module has been deprecated. Use 'vmware_guest' instead.", version=2.9)
    if (not HAS_PYSPHERE):
        module.fail_json(msg='pysphere module required')
    vcenter_hostname = module.params['vcenter_hostname']
    username = module.params['username']
    password = module.params['password']
    vmware_guest_facts = module.params['vmware_guest_facts']
    state = module.params['state']
    guest = module.params['guest']
    force = module.params['force']
    vm_disk = module.params['vm_disk']
    vm_nic = module.params['vm_nic']
    vm_hardware = module.params['vm_hardware']
    vm_extra_config = module.params['vm_extra_config']
    vm_hw_version = module.params['vm_hw_version']
    esxi = module.params['esxi']
    resource_pool = module.params['resource_pool']
    cluster = module.params['cluster']
    template_src = module.params['template_src']
    from_template = module.params['from_template']
    snapshot_to_clone = module.params['snapshot_to_clone']
    power_on_after_clone = module.params['power_on_after_clone']
    validate_certs = module.params['validate_certs']
    viserver = VIServer()
    if (validate_certs and (not hasattr(ssl, 'SSLContext')) and (not vcenter_hostname.startswith('http://'))):
        module.fail_json(msg='pysphere does not support verifying certificates with python < 2.7.9.  Either update python or set validate_certs=False on the task')
    if ((not validate_certs) and hasattr(ssl, 'SSLContext')):
        ssl._create_default_https_context = ssl._create_unverified_context
    try:
        viserver.connect(vcenter_hostname, username, password)
    except ssl.SSLError as sslerr:
        module.fail_json(msg=('Unable to validate the certificate of the vcenter hostname %s. Due to %s' % (vcenter_hostname, sslerr)))
    except socket.gaierror as err:
        module.fail_json(msg=('Unable to resolve name for vcenter hostname: %s. Due to %s' % (vcenter_hostname, to_native(err))))
    except (TypeError, VIApiException) as err:
        module.fail_json(msg=('Cannot connect to %s: %s' % (vcenter_hostname, to_native(err))), exception=traceback.format_exc())
    try:
        vm = viserver.get_vm_by_name(guest)
    except Exception:
        pass
    if vm:
        if vmware_guest_facts:
            try:
                module.exit_json(ansible_facts=gather_facts(vm))
            except Exception as e:
                module.fail_json(msg=('Fact gather failed with exception %s' % to_native(e)), exception=traceback.format_exc())
        elif (state in ['powered_on', 'powered_off', 'restarted']):
            state_result = power_state(vm, state, force)
            if isinstance(state_result, string_types):
                module.fail_json(msg=state_result)
            else:
                module.exit_json(changed=state_result)
        elif (state == 'present'):
            module.exit_json(changed=False)
        elif (state == 'reconfigured'):
            reconfigure_vm(vsphere_client=viserver, vm=vm, module=module, esxi=esxi, resource_pool=resource_pool, cluster_name=cluster, guest=guest, vm_extra_config=vm_extra_config, vm_hardware=vm_hardware, vm_disk=vm_disk, vm_nic=vm_nic, state=state, force=force)
        elif (state == 'absent'):
            delete_vm(vsphere_client=viserver, module=module, guest=guest, vm=vm, force=force)
    else:
        if vmware_guest_facts:
            module.fail_json(msg=('No such VM %s. Fact gathering requires an existing vm' % guest))
        elif from_template:
            deploy_template(vsphere_client=viserver, esxi=esxi, resource_pool=resource_pool, guest=guest, template_src=template_src, module=module, cluster_name=cluster, snapshot_to_clone=snapshot_to_clone, power_on_after_clone=power_on_after_clone, vm_extra_config=vm_extra_config)
        if (state in ['restarted', 'reconfigured']):
            module.fail_json(msg=('No such VM %s. States [restarted, reconfigured] required an existing VM' % guest))
        elif (state == 'absent'):
            module.exit_json(changed=False, msg=('vm %s not present' % guest))
        elif ((state in ['present', 'powered_off', 'powered_on']) and (not all((vm_extra_config, vm_hardware, vm_disk, vm_nic, esxi)))):
            module.exit_json(changed=False, msg=('vm %s not present' % guest))
        elif (state in ['present', 'powered_off', 'powered_on']):
            config_check('vm_disk', vm_disk, proto_vm_disk, module)
            config_check('vm_nic', vm_nic, proto_vm_nic, module)
            config_check('vm_hardware', vm_hardware, proto_vm_hardware, module)
            config_check('esxi', esxi, proto_esxi, module)
            create_vm(vsphere_client=viserver, module=module, esxi=esxi, resource_pool=resource_pool, cluster_name=cluster, guest=guest, vm_extra_config=vm_extra_config, vm_hardware=vm_hardware, vm_disk=vm_disk, vm_nic=vm_nic, vm_hw_version=vm_hw_version, state=state)
    viserver.disconnect()
    module.exit_json(changed=False, vcenter=vcenter_hostname)
