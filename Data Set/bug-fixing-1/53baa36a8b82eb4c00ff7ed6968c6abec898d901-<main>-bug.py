

def main():
    module = AnsibleModule(argument_spec=dict(instance_name=dict(required=True), snapshot_name=dict(required=True), state=dict(choices=['present', 'absent'], default='present'), disks=dict(default=None, type='list'), service_account_email=dict(type='str'), credentials_file=dict(type='path'), project_id=dict(type='str')))
    if (not HAS_LIBCLOUD):
        module.fail_json(msg='libcloud with GCE support (0.19.0+) is required for this module')
    gce = gce_connect(module)
    instance_name = module.params.get('instance_name')
    snapshot_name = module.params.get('snapshot_name')
    disks = module.params.get('disks')
    state = module.params.get('state')
    json_output = dict(changed=False, snapshots_created=[], snapshots_deleted=[], snapshots_existing=[], snapshots_absent=[])
    snapshot = None
    instance = gce.ex_get_node(instance_name, 'all')
    instance_disks = instance.extra['disks']
    for instance_disk in instance_disks:
        device_name = instance_disk['deviceName']
        if ((disks is None) or (device_name in disks)):
            volume_obj = gce.ex_get_volume(device_name)
            if (len(instance_disks) > 1):
                snapshot_name = ((device_name + '-') + snapshot_name)
            snapshot = find_snapshot(volume_obj, snapshot_name)
            if (snapshot and (state == 'present')):
                json_output['snapshots_existing'].append(snapshot_name)
            elif (snapshot and (state == 'absent')):
                snapshot.destroy()
                json_output['changed'] = True
                json_output['snapshots_deleted'].append(snapshot_name)
            elif ((not snapshot) and (state == 'present')):
                volume_obj.snapshot(snapshot_name)
                json_output['changed'] = True
                json_output['snapshots_created'].append(snapshot_name)
            elif ((not snapshot) and (state == 'absent')):
                json_output['snapshots_absent'].append(snapshot_name)
    module.exit_json(**json_output)
