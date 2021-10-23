def main():
    module = AnsibleModule(argument_spec=dict(account_api_token=dict(required=True, no_log=True, type='str'), account_email=dict(required=True, type='str'), port=dict(required=False, default=None, type='int'), priority=dict(required=False, default=1, type='int'), proto=dict(required=False, default=None, choices=['tcp', 'udp'], type='str'), proxied=dict(required=False, default=False, type='bool'), record=dict(required=False, default='@', aliases=['name'], type='str'), service=dict(required=False, default=None, type='str'), solo=dict(required=False, default=None, type='bool'), state=dict(required=False, default='present', choices=['present', 'absent'], type='str'), timeout=dict(required=False, default=30, type='int'), ttl=dict(required=False, default=1, type='int'), type=dict(required=False, default=None, choices=['A', 'AAAA', 'CNAME', 'TXT', 'SRV', 'MX', 'NS', 'SPF'], type='str'), value=dict(required=False, default=None, aliases=['content'], type='str'), weight=dict(required=False, default=1, type='int'), zone=dict(required=True, default=None, aliases=['domain'], type='str')), supports_check_mode=True, required_if=[('state', 'present', ['record', 'type', 'value']), ('state', 'absent', ['record']), ('type', 'SRV', ['proto', 'service'])])
    if (module.params['type'] == 'SRV'):
        if (not (((module.params['weight'] is not None) and (module.params['port'] is not None) and (not ((module.params['value'] is None) or (module.params['value'] == '')))) or ((module.params['weight'] is None) and (module.params['port'] is None) and ((module.params['value'] is None) or (module.params['value'] == ''))))):
            module.fail_json(msg='For SRV records the params weight, port and value all need to be defined, or not at all.')
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
        else:
            module.exit_json(changed=changed, result={
                'record': result,
            })
    else:
        changed = cf_api.delete_dns_records(solo=False)
        module.exit_json(changed=changed)