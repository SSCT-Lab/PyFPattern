

def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(group=dict(type='str'), node=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'present', 'query']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'absent', ['node', 'group']], ['state', 'present', ['node', 'group']]])
    state = module.params['state']
    group = module.params['group']
    node = module.params['node']
    aci = ACIModule(module)
    aci.construct_url(root_class=dict(aci_class='maintMaintGrp', aci_rn='fabric/maintgrp-{0}'.format(group), target_filter={
        'name': group,
    }, module_object=group), subclass_1=dict(aci_class='fabricNodeBlk', aci_rn='nodeblk-blk{0}-{0}'.format(node), target_filter={
        'name': 'blk{0}-{0}'.format(node),
    }, module_object=node))
    aci.get_existing()
    if (state == 'present'):
        aci.payload(aci_class='fabricNodeBlk', class_config=dict(from_=node, to_=node))
        aci.get_diff(aci_class='fabricNodeBlk')
        aci.post_config()
    elif (state == 'absent'):
        aci.delete_config()
    aci.exit_json()
