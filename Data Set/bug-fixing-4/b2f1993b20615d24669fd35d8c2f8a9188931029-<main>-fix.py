def main():
    argument_spec = ipa_argument_spec()
    argument_spec.update(zone_name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['present', 'absent']), dynamicupdate=dict(type='str', required=False, default='false', choices=['true', 'false']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    client = DNSZoneIPAClient(module=module, host=module.params['ipa_host'], port=module.params['ipa_port'], protocol=module.params['ipa_prot'])
    try:
        client.login(username=module.params['ipa_user'], password=module.params['ipa_pass'])
        (changed, zone) = ensure(module, client)
        module.exit_json(changed=changed, zone=zone)
    except Exception as e:
        module.fail_json(msg=to_native(e))