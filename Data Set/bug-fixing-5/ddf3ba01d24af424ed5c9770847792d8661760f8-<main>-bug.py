def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(description=dict(type='str', aliases=['descr']), node_id=dict(type='int'), pod_id=dict(type='int'), role=dict(type='str', choices=['leaf', 'spine', 'unspecified'], aliases=['role_name']), serial=dict(type='str', aliases=['serial_number']), switch=dict(type='str', aliases=['name', 'switch_name']), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['node_id', 'serial']], ['state', 'present', ['node_id', 'serial']]])
    pod_id = module.params['pod_id']
    serial = module.params['serial']
    node_id = module.params['node_id']
    switch = module.params['switch']
    description = module.params['description']
    role = module.params['role']
    state = module.params['state']
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class='fabricNodeIdentP', aci_rn='controller/nodeidentpol/nodep-{0}'.format(serial), module_object=serial, target_filter={
        'serial': serial,
    }))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fabricNodeIdentP', class_config=dict(descr=description, name=switch, nodeId=node_id, podId=pod_id, rn='nodep-{0}'.format(serial), role=role, serial=serial))
        aci.get_diff(aci_class='fabricNodeIdentP')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json(**aci.result)