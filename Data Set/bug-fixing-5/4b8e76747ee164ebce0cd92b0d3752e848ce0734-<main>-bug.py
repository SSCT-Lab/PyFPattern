def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(description=dict(type='str', aliases=['descr']), export_policy=dict(type='str', aliases=['name']), format=dict(type='str', choices=['json', 'xml']), include_secure=dict(type='str', choices=['no', 'yes']), max_count=dict(type='int'), snapshot=dict(type='str'), state=dict(type='str', choices=['absent', 'present', 'query'], default='present'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, required_if=[['state', 'absent', ['export_policy', 'snapshot']], ['state', 'present', ['export_policy']]])
    description = module.params['description']
    export_policy = module.params['export_policy']
    file_format = module.params['format']
    include_secure = module.params['include_secure']
    max_count = module.params['max_count']
    if (max_count is not None):
        if (max_count in range(1, 11)):
            max_count = str(max_count)
        else:
            module.fail_json(msg='The "max_count" must be a number between 1 and 10')
    snapshot = module.params['snapshot']
    if ((snapshot is not None) and (not snapshot.startswith('run-'))):
        snapshot = ('run-' + snapshot)
    state = module.params['state']
    aci = ACIModule(module)
    if (state == 'present'):
        aci.construct_url(root_class=dict(aci_class='configExportP', aci_rn='fabric/configexp-{0}'.format(export_policy), filter_target='eq(configExportP.name, "{0}")'.format(export_policy), module_object=export_policy))
        aci.get_existing()
        aci.payload(aci_class='configExportP', class_config=dict(adminSt='triggered', descr=description, format=file_format, includeSecureFields=include_secure, maxSnapshotCount=max_count, name=export_policy, snapshot='yes'))
        aci.get_diff('configExportP')
        aci.post_config()
    else:
        if (export_policy is not None):
            export_policy = 'uni/fabric/configexp-{0}'.format(export_policy)
        aci.construct_url(root_class=dict(aci_class='configSnapshotCont', aci_rn='backupst/snapshots-[{0}]'.format(export_policy), filter_target='(configSnapshotCont.name, "{0}")'.format(export_policy), module_object=export_policy), subclass_1=dict(aci_class='configSnapshot', aci_rn='snapshot-{0}'.format(snapshot), filter_target='(configSnapshot.name, "{0}")'.format(snapshot), module_object=snapshot))
        aci.get_existing()
        if (state == 'absent'):
            aci.payload(aci_class='configSnapshot', class_config=dict(name=snapshot, retire='yes'))
            if aci.result['existing']:
                aci.get_diff('configSnapshot')
                aci.post_config()
    module.exit_json(**aci.result)