def main():
    module = AnsibleModule(argument_spec=dict(account_api_token=dict(type='str', required=True, no_log=True), account_email=dict(type='str', required=True), algorithm=dict(type='int'), cert_usage=dict(type='int', choices=[0, 1, 2, 3]), hash_type=dict(type='int', choices=[1, 2]), key_tag=dict(type='int'), port=dict(type='int'), priority=dict(type='int', default=1), proto=dict(type='str'), proxied=dict(type='bool', default=False), record=dict(type='str', default='@', aliases=['name']), selector=dict(type='int', choices=[0, 1]), service=dict(type='str'), solo=dict(type='bool'), state=dict(type='str', default='present', choices=['absent', 'present']), timeout=dict(type='int', default=30), ttl=dict(type='int', default=1), type=dict(type='str', choices=['A', 'AAAA', 'CNAME', 'DS', 'MX', 'NS', 'SPF', 'SRV', 'SSHFP', 'TLSA', 'TXT']), value=dict(type='str', aliases=['content']), weight=dict(type='int', default=1), zone=dict(type='str', required=True, aliases=['domain'])), supports_check_mode=True, required_if=([('state', 'present', ['record', 'type', 'value']), ('state', 'absent', ['record']), ('type', 'SRV', ['proto', 'service']), ('type', 'TLSA', ['proto', 'port'])],))
    if (module.params['type'] == 'SRV'):
        if (not (((module.params['weight'] is not None) and (module.params['port'] is not None) and (not ((module.params['value'] is None) or (module.params['value'] == '')))) or ((module.params['weight'] is None) and (module.params['port'] is None) and ((module.params['value'] is None) or (module.params['value'] == ''))))):
            module.fail_json(msg='For SRV records the params weight, port and value all need to be defined, or not at all.')
    if (module.params['type'] == 'SSHFP'):
        if (not (((module.params['algorithm'] is not None) and (module.params['hash_type'] is not None) and (not ((module.params['value'] is None) or (module.params['value'] == '')))) or ((module.params['algorithm'] is None) and (module.params['hash_type'] is None) and ((module.params['value'] is None) or (module.params['value'] == ''))))):
            module.fail_json(msg='For SSHFP records the params algorithm, hash_type and value all need to be defined, or not at all.')
    if (module.params['type'] == 'TLSA'):
        if (not (((module.params['cert_usage'] is not None) and (module.params['selector'] is not None) and (module.params['hash_type'] is not None) and (not ((module.params['value'] is None) or (module.params['value'] == '')))) or ((module.params['cert_usage'] is None) and (module.params['selector'] is None) and (module.params['hash_type'] is None) and ((module.params['value'] is None) or (module.params['value'] == ''))))):
            module.fail_json(msg='For TLSA records the params cert_usage, selector, hash_type and value all need to be defined, or not at all.')
    if (module.params['type'] == 'DS'):
        if (not (((module.params['key_tag'] is not None) and (module.params['algorithm'] is not None) and (module.params['hash_type'] is not None) and (not ((module.params['value'] is None) or (module.params['value'] == '')))) or ((module.params['key_tag'] is None) and (module.params['algorithm'] is None) and (module.params['hash_type'] is None) and ((module.params['value'] is None) or (module.params['value'] == ''))))):
            module.fail_json(msg='For DS records the params key_tag, algorithm, hash_type and value all need to be defined, or not at all.')
    changed = False
    cf_api = CloudflareAPI(module)
    if (cf_api.is_solo and (cf_api.state == 'absent')):
        module.fail_json(msg='solo=true can only be used with state=present')
    if (cf_api.state == 'present'):
        if cf_api.is_solo:
            changed = cf_api.delete_dns_records(solo=cf_api.is_solo)
        (result, changed) = cf_api.ensure_dns_record()
        if isinstance(result, list):
            module.exit_json(changed=changed, result={
                'record': result[0],
            })
        module.exit_json(changed=changed, result={
            'record': result,
        })
    else:
        changed = cf_api.delete_dns_records(solo=False)
        module.exit_json(changed=changed)