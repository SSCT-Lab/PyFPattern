def main():
    module = AnsibleModule(supports_check_mode=True, argument_spec=dict(table=dict(type='str', default='filter', choices=['filter', 'nat', 'mangle', 'raw', 'security']), state=dict(type='str', default='present', choices=['absent', 'present']), action=dict(type='str', default='append', choices=['append', 'insert']), ip_version=dict(type='str', default='ipv4', choices=['ipv4', 'ipv6']), chain=dict(type='str'), protocol=dict(type='str'), source=dict(type='str'), to_source=dict(type='str'), destination=dict(type='str'), to_destination=dict(type='str'), match=dict(type='list', default=[]), tcp_flags=dict(type='dict', default={
        
    }), jump=dict(type='str'), log_prefix=dict(type='str'), goto=dict(type='str'), in_interface=dict(type='str'), out_interface=dict(type='str'), fragment=dict(type='str'), set_counters=dict(type='str'), source_port=dict(type='str'), destination_port=dict(type='str'), to_ports=dict(type='str'), set_dscp_mark=dict(type='str'), set_dscp_mark_class=dict(type='str'), comment=dict(type='str'), ctstate=dict(type='list', default=[]), limit=dict(type='str'), limit_burst=dict(type='str'), uid_owner=dict(type='str'), reject_with=dict(type='str'), icmp_type=dict(type='str'), syn=dict(type='str', default='ignore', choices=['ignore', 'match', 'negate']), flush=dict(type='bool', default=False), policy=dict(type='str', choices=['ACCEPT', 'DROP', 'QUEUE', 'RETURN'])), mutually_exclusive=(['set_dscp_mark', 'set_dscp_mark_class'], ['flush', 'policy']))
    args = dict(changed=False, failed=False, ip_version=module.params['ip_version'], table=module.params['table'], chain=module.params['chain'], flush=module.params['flush'], rule=' '.join(construct_rule(module.params)), state=module.params['state'])
    ip_version = module.params['ip_version']
    iptables_path = module.get_bin_path(BINS[ip_version], True)
    if ((args['flush'] is False) and (args['chain'] is None)):
        module.fail_json(msg='Either chain or flush parameter must be specified.')
    if (args['flush'] is True):
        args['changed'] = True
        if (not module.check_mode):
            flush_table(iptables_path, module, module.params)
    elif module.params['policy']:
        current_policy = get_chain_policy(iptables_path, module, module.params)
        if (not current_policy):
            module.fail_json(msg="Can't detect current policy")
        changed = (current_policy != module.params['policy'])
        args['changed'] = changed
        if (changed and (not module.check_mode)):
            set_chain_policy(iptables_path, module, module.params)
    else:
        insert = (module.params['action'] == 'insert')
        rule_is_present = check_present(iptables_path, module, module.params)
        should_be_present = (args['state'] == 'present')
        args['changed'] = (rule_is_present != should_be_present)
        if (args['changed'] is False):
            module.exit_json(**args)
        if (not module.check_mode):
            if should_be_present:
                if insert:
                    insert_rule(iptables_path, module, module.params)
                else:
                    append_rule(iptables_path, module, module.params)
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