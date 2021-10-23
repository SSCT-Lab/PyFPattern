

def main():
    'Main function'
    module = GcpModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), can_ip_forward=dict(type='bool'), disks=dict(type='list', elements='dict', options=dict(auto_delete=dict(type='bool'), boot=dict(type='bool'), device_name=dict(type='str'), disk_encryption_key=dict(type='dict', options=dict(raw_key=dict(type='str'), rsa_encrypted_key=dict(type='str'), sha256=dict(type='str'))), index=dict(type='int'), initialize_params=dict(type='dict', options=dict(disk_name=dict(type='str'), disk_size_gb=dict(type='int'), disk_type=dict(type='str'), source_image=dict(type='str'), source_image_encryption_key=dict(type='dict', options=dict(raw_key=dict(type='str'), sha256=dict(type='str'))))), interface=dict(type='str', choices=['SCSI', 'NVME']), mode=dict(type='str', choices=['READ_WRITE', 'READ_ONLY']), source=dict(type='dict'), type=dict(type='str', choices=['SCRATCH', 'PERSISTENT']))), guest_accelerators=dict(type='list', elements='dict', options=dict(accelerator_count=dict(type='int'), accelerator_type=dict(type='str'))), label_fingerprint=dict(type='str'), metadata=dict(type='dict'), machine_type=dict(type='str'), min_cpu_platform=dict(type='str'), name=dict(type='str'), network_interfaces=dict(type='list', elements='dict', options=dict(access_configs=dict(type='list', elements='dict', options=dict(name=dict(required=True, type='str'), nat_ip=dict(required=True, type='dict'), type=dict(required=True, type='str', choices=['ONE_TO_ONE_NAT']))), alias_ip_ranges=dict(type='list', elements='dict', options=dict(ip_cidr_range=dict(type='str'), subnetwork_range_name=dict(type='str'))), name=dict(type='str'), network=dict(type='dict'), network_ip=dict(type='str'), subnetwork=dict(type='dict'))), scheduling=dict(type='dict', options=dict(automatic_restart=dict(type='bool'), on_host_maintenance=dict(type='str'), preemptible=dict(type='bool'))), service_accounts=dict(type='list', elements='dict', options=dict(email=dict(type='str'), scopes=dict(type='list', elements='str'))), tags=dict(type='dict', options=dict(fingerprint=dict(type='str'), items=dict(type='list', elements='str'))), zone=dict(required=True, type='str')))
    state = module.params['state']
    kind = 'compute#instance'
    fetch = fetch_resource(module, self_link(module), kind)
    changed = False
    if fetch:
        if (state == 'present'):
            if is_different(module, fetch):
                fetch = update(module, self_link(module), kind, fetch)
                changed = True
        else:
            delete(module, self_link(module), kind, fetch)
            fetch = {
                
            }
            changed = True
    elif (state == 'present'):
        fetch = create(module, collection(module), kind)
        changed = True
    else:
        fetch = {
            
        }
    fetch.update({
        'changed': changed,
    })
    module.exit_json(**fetch)
