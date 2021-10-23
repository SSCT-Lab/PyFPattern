def main():
    module = AnsibleModule(supports_check_mode=True, argument_spec=dict(table=dict(required=False, default='filter', choices=['filter', 'nat', 'mangle', 'raw', 'security']), state=dict(required=False, default='present', choices=['present', 'absent']), action=dict(required=False, default='append', type='str', choices=['append', 'insert']), ip_version=dict(required=False, default='ipv4', choices=['ipv4', 'ipv6']), chain=dict(required=False, default=None, type='str'), protocol=dict(required=False, default=None, type='str'), source=dict(required=False, default=None, type='str'), to_source=dict(required=False, default=None, type='str'), destination=dict(required=False, default=None, type='str'), to_destination=dict(required=False, default=None, type='str'), match=dict(required=False, default=[], type='list'), jump=dict(required=False, default=None, type='str'), goto=dict(required=False, default=None, type='str'), in_interface=dict(required=False, default=None, type='str'), out_interface=dict(required=False, default=None, type='str'), fragment=dict(required=False, default=None, type='str'), set_counters=dict(required=False, default=None, type='str'), source_port=dict(required=False, default=None, type='str'), destination_port=dict(required=False, default=None, type='str'), to_ports=dict(required=False, default=None, type='str'), set_dscp_mark=dict(required=False, default=None, type='str'), set_dscp_mark_class=dict(required=False, default=None, type='str'), comment=dict(required=False, default=None, type='str'), ctstate=dict(required=False, default=[], type='list'), limit=dict(required=False, default=None, type='str'), limit_burst=dict(required=False, default=None, type='str'), uid_owner=dict(required=False, default=None, type='str'), reject_with=dict(required=False, default=None, type='str'), icmp_type=dict(required=False, default=None, type='str'), flush=dict(required=False, default=False, type='bool'), policy=dict(required=False, default=None, type='str', choices=['ACCEPT', 'DROP', 'QUEUE', 'RETURN'])), mutually_exclusive=(['set_dscp_mark', 'set_dscp_mark_class'], ['flush', 'policy']))
    args = dict(changed=False, failed=False, ip_version=module.params['ip_version'], table=module.params['table'], chain=module.params['chain'], flush=module.params['flush'], rule=' '.join(construct_rule(module.params)), state=module.params['state'])
    ip_version = module.params['ip_version']
    iptables_path = module.get_bin_path(BINS[ip_version], True)
    if ((args['flush'] is False) and (args['chain'] is None)):
        module.fail_json(msg='Either chain or flush parameter must be specified.')
    if args['flush']:
        args['changed'] = True
        if (not module.check_mode):
            flush_table(iptables_path, module, module.params)
    elif module.params['policy']:
        args['changed'] = True
        if (not module.check_mode):
            set_chain_policy(iptables_path, module, module.params)
    else:
        insert = (module.params['action'] == 'insert')
        rule_is_present = check_present(iptables_path, module, module.params)
        should_be_present = (args['state'] == 'present')
        args['changed'] = (rule_is_present != should_be_present)
        if (args['changed'] and (not module.check_mode)):
            if should_be_present:
                if insert:
                    insert_rule(iptables_path, module, module.params)
                else:
                    append_rule(iptables_path, module, module.params)
            else:
                remove_rule(iptables_path, module, module.params)
    module.exit_json(**args)