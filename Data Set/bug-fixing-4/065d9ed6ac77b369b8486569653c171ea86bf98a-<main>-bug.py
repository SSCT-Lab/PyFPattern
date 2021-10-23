def main():
    record_types = ['A', 'AAAA', 'A6', 'CNAME', 'DNAME', 'PTR', 'TXT']
    argument_spec = ipa_argument_spec()
    argument_spec.update(zone_name=dict(type='str', required=True), record_name=dict(type='str', aliases=['name'], required=True), record_type=dict(type='str', default='A', choices=record_types), record_value=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    client = DNSRecordIPAClient(module=module, host=module.params['ipa_host'], port=module.params['ipa_port'], protocol=module.params['ipa_prot'])
    try:
        client.login(username=module.params['ipa_user'], password=module.params['ipa_pass'])
        (changed, record) = ensure(module, client)
        module.exit_json(changed=changed, record=record)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())