

def main():
    tsig_algs = ['HMAC-MD5.SIG-ALG.REG.INT', 'hmac-md5', 'hmac-sha1', 'hmac-sha224', 'hmac-sha256', 'hamc-sha384', 'hmac-sha512']
    module = AnsibleModule(argument_spec=dict(state=dict(required=False, default='present', choices=['present', 'absent'], type='str'), server=dict(required=True, type='str'), key_name=dict(required=False, type='str'), key_secret=dict(required=False, type='str', no_log=True), key_algorithm=dict(required=False, default='hmac-md5', choices=tsig_algs, type='str'), zone=dict(required=True, type='str'), record=dict(required=True, type='str'), type=dict(required=False, default='A', type='str'), ttl=dict(required=False, default=3600, type='int'), value=dict(required=False, default=None, type='str')), supports_check_mode=True)
    if (not HAVE_DNSPYTHON):
        module.fail_json(msg='python library dnspython required: pip install dnspython')
    if (len(module.params['record']) == 0):
        module.fail_json(msg='record cannot be empty.')
    record = RecordManager(module)
    result = {
        
    }
    if (module.params['state'] == 'absent'):
        result = record.remove_record()
    elif (module.params['state'] == 'present'):
        result = record.create_or_update_record()
    result['dns_rc'] = record.dns_rc
    result['dns_rc_str'] = dns.rcode.to_text(record.dns_rc)
    if result['failed']:
        module.fail_json(**result)
    else:
        result['record'] = dict(zone=record.zone, record=module.params['record'], type=module.params['type'], ttl=module.params['ttl'], value=module.params['value'])
        module.exit_json(**result)
