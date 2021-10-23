

def main():
    argument_spec = dict(comment=dict(type='str'), id=dict(type='int', required=True), src_intf=dict(default='any'), dst_intf=dict(default='any'), state=dict(choices=['present', 'absent'], default='present'), src_addr=dict(required=True, type='list'), dst_addr=dict(required=True, type='list'), src_addr_negate=dict(type='bool', default=False), dst_addr_negate=dict(type='bool', default=False), policy_action=dict(choices=['accept', 'deny'], required=True, aliases=['action']), service=dict(aliases=['services'], required=True, type='list'), service_negate=dict(type='bool', default=False), schedule=dict(type='str', default='always'), nat=dict(type='bool', default=False), fixedport=dict(type='bool', default=False), poolname=dict(type='str'), av_profile=dict(type='str'), webfilter_profile=dict(type='str'), ips_sensor=dict(type='str'), application_list=dict(type='str'))
    argument_spec.update(fortios_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=fortios_required_if)
    fortigate = AnsibleFortios(module)
    if (not module.params['nat']):
        if module.params['poolname']:
            module.fail_json(msg='Poolname param requires NAT to be true.')
        if module.params['fixedport']:
            module.fail_json(msg='Fixedport param requires NAT to be true.')
    policy_id = str(module.params['id'])
    fortigate.load_config('firewall policy')
    if (module.params['state'] == 'absent'):
        fortigate.candidate_config[path].del_block(policy_id)
    elif (module.params['state'] == 'present'):
        new_policy = fortigate.get_empty_configuration_block(policy_id, 'edit')
        new_policy.set_param('srcintf', ('"%s"' % module.params['src_intf']))
        new_policy.set_param('dstintf', ('"%s"' % module.params['dst_intf']))
        new_policy.set_param('srcaddr', ' '.join(((('"' + item) + '"') for item in module.params['src_addr'])))
        new_policy.set_param('dstaddr', ' '.join(((('"' + item) + '"') for item in module.params['dst_addr'])))
        new_policy.set_param('service', ' '.join(((('"' + item) + '"') for item in module.params['service'])))
        if module.params['src_addr_negate']:
            new_policy.set_param('srcaddr-negate', 'enable')
        if module.params['dst_addr_negate']:
            new_policy.set_param('dstaddr-negate', 'enable')
        if module.params['service_negate']:
            new_policy.set_param('service-negate', 'enable')
        new_policy.set_param('action', ('%s' % module.params['policy_action']))
        new_policy.set_param('schedule', ('%s' % module.params['schedule']))
        if module.params['nat']:
            new_policy.set_param('nat', 'enable')
            if module.params['fixedport']:
                new_policy.set_param('fixedport', 'enable')
            if (module.params['poolname'] is not None):
                new_policy.set_param('ippool', 'enable')
                new_policy.set_param('poolname', ('"%s"' % module.params['poolname']))
        if (module.params['av_profile'] is not None):
            new_policy.set_param('av-profile', ('"%s"' % module.params['av_profile']))
        if (module.params['webfilter_profile'] is not None):
            new_policy.set_param('webfilter-profile', ('"%s"' % module.params['webfilter_profile']))
        if (module.params['ips_sensor'] is not None):
            new_policy.set_param('ips-sensor', ('"%s"' % module.params['ips_sensor']))
        if (module.params['application_list'] is not None):
            new_policy.set_param('application-list', ('"%s"' % module.params['application_list']))
        if (module.params['comment'] is not None):
            new_policy.set_param('comment', ('"%s"' % module.params['comment']))
        fortigate.add_block(policy_id, new_policy)
    fortigate.apply_changes()
